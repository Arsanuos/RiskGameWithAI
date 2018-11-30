document.onload = (function(d3, saveAs, Blob, undefined){
  "use strict";
  
  // TODO add user settings
  var consts = {
    defaultTitle: "0",
    defaultUnkown: "-1",
  };
  var settings = {
    appendElSpec: "#graph"
  };

  
  // define graphcreator object
  var GraphCreator = function(svg, nodes, edges, partitions){
    var thisGraph = this;
        thisGraph.idct = 0;
    
        var players = ["Player 1", "Player 2"];

    thisGraph.nodes = nodes || [];
    thisGraph.edges = edges || [];
    thisGraph.partitions = partitions || []

    thisGraph.state = {
      selectedNode: null,
      selectedEdge: null,
      mouseDownNode: null,
      mouseDownLink: null,
      justDragged: false,
      justScaleTransGraph: false,
      lastKeyDown: -1,
      shiftNodeDrag: false,
      selectedText: null,
      currentPlayer: 0,
      bonusVal: 10,
      bonusNode: null,
      prevNode: null,
      moveFromNode: null,
      moveToNode: null,
      movedArmies: null,
      attackerNode: null,
      attackedNode: null,
      attackedNodeArmies: -1,
      algo1: null,
      algo2: null,

    };


    // define arrow markers for graph links
    var defs = svg.append('svg:defs');
    defs.append('svg:marker')
      //.attr('id', 'end-arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', "32")
      .attr('markerWidth', 3.5)
      .attr('markerHeight', 3.5)
      .attr('orient', 'auto')
      .append('svg:path')
      .attr('d', 'M0,-5L10,0L0,5');


    // define arrow markers for leading arrow
    defs.append('svg:marker')
      //.attr('id', 'mark-end-arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 7)
      .attr('markerWidth', 3.5)
      .attr('markerHeight', 3.5)
      .attr('orient', 'auto')
      .append('svg:path')
      .attr('d', 'M0,-5L10,0L0,5');

    thisGraph.svg = svg;
    thisGraph.svgG = svg.append("g")
          .classed(thisGraph.consts.graphClass, true);
    var svgG = thisGraph.svgG;

    // displayed when dragging between nodes
    thisGraph.dragLine = svgG.append('svg:path')
          .attr('class', 'link dragline hidden')
          .attr('d', 'M0,0L0,0')
          //.style('marker-end', 'url(#mark-end-arrow)');

    // svg nodes and edges
    thisGraph.paths = svgG.append("g").selectAll("g");
    thisGraph.circles = svgG.append("g").selectAll("g");

    thisGraph.drag = d3.behavior.drag()
          .origin(function(d){
            return {x: d.x, y: d.y};
          })
          .on("drag", function(args){
            thisGraph.state.justDragged = true;
            thisGraph.dragmove.call(thisGraph, args);
          })
          .on("dragend", function() {
            // todo check if edge-mode is selected
          });

    // listen for key events
    d3.select(window).on("keydown", function(){
      thisGraph.svgKeyDown.call(thisGraph);
    })
    .on("keyup", function(){
      thisGraph.svgKeyUp.call(thisGraph);
    });
    svg.on("mousedown", function(d){thisGraph.svgMouseDown.call(thisGraph, d);});
    svg.on("mouseup", function(d){thisGraph.svgMouseUp.call(thisGraph, d);});

    // listen for dragging
    var dragSvg = d3.behavior.zoom()
          .on("zoom", function(){
            if (d3.event.sourceEvent.shiftKey){
              // TODO  the internal d3 state is still changing
              return false;
            } else{
              thisGraph.zoomed.call(thisGraph);
            }
            return true;
          })
          .on("zoomstart", function(){
            var ael = d3.select("#" + thisGraph.consts.activeEditId).node();
            if (ael){
              ael.blur();
            }
            if (!d3.event.sourceEvent.shiftKey) d3.select('body').style("cursor", "move");
          })
          .on("zoomend", function(){
            d3.select('body').style("cursor", "auto");
          });

    svg.call(dragSvg).on("dblclick.zoom", null);

    // listen for resize
    window.onresize = function(){thisGraph.updateWindow(svg);};

    // handle download data
    d3.select("#download-input").on("click", function(){
      var saveEdges = [];
      thisGraph.edges.forEach(function(val, i){
        saveEdges.push([val.source.id, val.target.id]);
      });
      var tmp = []
      thisGraph.nodes.forEach(function(node){
        tmp.push({id:node.id, title:node.title, x:node.x, y:node.y, player:node.player});
      });
      // TODO:: Add algorithms.
      var blob = new Blob([window.JSON.stringify({"nodes": tmp, "edges": saveEdges, "partitions":thisGraph.partitions,
       "algo1":thisGraph.state.algo1, "algo2":thisGraph.state.algo2})], 
      {type: "text/plain;charset=utf-8"});
      saveAs(blob, "mydag.json");
    });


    // handle uploaded data
    d3.select("#upload-input").on("click", function(){
      document.getElementById("hidden-file-upload").click();
    });

    function loadUi(){
      let textAreaVal = "";
      thisGraph.partitions.forEach(function(partition){
        textAreaVal += partition.join(" ") + "\n";
      });
      $("#partitions").text(textAreaVal);
      $("#p1Algo").val(thisGraph.state.algo1);
      $("#p2Algo").val(thisGraph.state.algo2);
    }

    d3.select("#hidden-file-upload").on("change", function(){
      if (window.File && window.FileReader && window.FileList && window.Blob) {
        var uploadFile = this.files[0];
        var filereader = new window.FileReader();

        filereader.onload = function(){
          var txtRes = filereader.result;
          // TODO better error handling
          try{
            var jsonObj = JSON.parse(txtRes);
            thisGraph.deleteGraph(true);
            thisGraph.nodes = jsonObj.nodes;
            /*thisGraph.nodes.forEach(function(node){
              node.title = node.title;
              return node;
            });*/
            thisGraph.setIdCt(jsonObj.nodes.length + 1);
            var newEdges = jsonObj.edges;
            newEdges.forEach(function(e, i){
              newEdges[i] = {source: thisGraph.nodes.filter(function(n){return n.id == e[0];})[0],
                          target: thisGraph.nodes.filter(function(n){return n.id == e[1];})[0]};
            });
            thisGraph.edges = newEdges;
            thisGraph.updateGraph();

            thisGraph.partitions = jsonObj.partitions;
            thisGraph.state.algo1 = jsonObj.algo1;
            thisGraph.state.algo2 = jsonObj.algo2;
            loadUi();
          }catch(err){
            window.alert("Error parsing uploaded file\nerror message: " + err.message);
            return;
          }
        };
        filereader.readAsText(uploadFile);

      } else {
        alert("Your browser won't let you save this graph -- try upgrading your browser to IE 10+ or Chrome or Firefox.");
      }

    });

    // handle delete graph
    d3.select("#delete-graph").on("click", function(){
      thisGraph.deleteGraph(false);
    });
    
    // handle submit event
    $("#submit").click(function(){
      thisGraph.partitions = [];
      $("#partitions").val().split("\n").forEach(function(val, index, arr){
        var ret = val.trim().split(" ");
        if(ret[0] != ""){
          thisGraph.partitions.push(ret);
        }
      });
    });

    $("#selectPlayer").change(function(){
      //color circles on select.
      thisGraph.circles.filter(function(cd){
        if(thisGraph.state.selectedNode){
          thisGraph.state.selectedNode.player = $('#selectPlayer :selected').text();
          return cd.id === thisGraph.state.selectedNode.id;
        }
      }).forEach(function(g){
        if(g[0] !== undefined){
          $(g[0].childNodes[0]).css("fill", $('#selectPlayer :selected').text() == "Player 1" ? "#d39e00" : "#299a43");
        }
        $("#selectPlayer").val("selectOption1");
      });
    });


    function sendPost(data, type){
      $.ajax({
        type: "POST",
        url: 'http://localhost:8000/',
        data: {json:JSON.stringify(data), type:type},
      }).fail(function(){
        //failure();
      }).done(function(response) {
        console.log(response.nodes);
        if(response.status == "valid"){
          thisGraph.nodes = response.nodes.sort(function(a, b){
            return a.id - b.id;
          });
          thisGraph.state.currentPlayer = response.player - 1;
          $("#nextPlayer").text("Player " + String(response.player + " turn."));
          thisGraph.state.bonusVal = response.bonus;
          thisGraph.updateGraph();
          updateBonusUi();
        }else if(response.status == "winner"){
          //TODO:: handle winner.
        } else {
          let error = "";
          response.error.forEach(function(message){
            error +=  "\n" + message;
          });
          $("#alerts").text(error);
          $("#alerts").fadeIn(700);
          $("#alerts").fadeOut(700);
        }
      });
    }

    function nextPlayer(){
      thisGraph.state.currentPlayer = (thisGraph.state.currentPlayer + 1) % 2;
    }

    $("#initialize").click(function(){
      intialState();

    });

    //handle doing actions.
    var firstReq = true;
    
    function intialState(){
      if(firstReq){
        //send all data.
        //turn exists only for humans.
        //response:
        //human -> next turn of AI
        //else all computation must be done in back-end as further request has nothing.
        //TODO:: human vs human.
        var nodes = [];
        thisGraph.nodes.forEach(function(curr){
          nodes.push({id:curr.id, title:curr.title, player:curr.player, x:curr.x, y:curr.y});
        });
        let data = {nodes:nodes, partitions:thisGraph.partitions, edges:thisGraph.edges, 
          p1:$('#p1Algo').find(":selected").text(), p2:$('#p2Algo').find(":selected").text()};
        sendPost(data, "state")
        firstReq = false;
      }
    }

    function handleTurn(){
      let turn = {bonusNode:thisGraph.bonusNode, 
        attackerNode:thisGraph.state.attackerNode, attackedNode:thisGraph.attackedNode,
         moveFromNode:thisGraph.moveFromNode, moveToNode:thisGraph.moveToNode,
         movedArmies:thisGraph.movedArmies, 
         attackedNodeArmies:thisGraph.state.attackedNodeArmies};
         sendPost(turn, "turn");
    }

    function getArmy(node){
      return Number(node.title);
    }

    function getOldColor(node){
      if((thisGraph.state.attackedNode != null && node.id == thisGraph.state.attackedNode.id) 
        || (thisGraph.state.attackerNode != null && node.id == thisGraph.state.attackerNode.id)){
        return "red";
      } else if((thisGraph.state.moveToNode != null && node.id == thisGraph.state.moveToNode.id)
        || (thisGraph.state.moveFromNode != null && node.id == thisGraph.state.moveFromNode.id)){
        return "blue";
      }else if(node.player == "Player 1"){
        return "#d39e00";
      }else if(node.player == "Player 2"){
        return "#299a43";
      }else{
        //default color.
        //return nothing to not over write parent color behaviour.
        return "";
      }
    }

    function colorNode(node, color){
      if(node == null){
        return;
      }
      thisGraph.circles[0].parentNode.childNodes.forEach(function(g, i){
        //if nodes exists.
        if(g !== undefined){
          //color node with color.
          console.log(node);
          if(node !== undefined && node.id == thisGraph.nodes[i].id){
            $(g.childNodes[0]).css("fill", color);
          }
        }
      });
    }

    function removeColorExcpetFrom(exceptNodes){
      if(exceptNodes.length == 1 && exceptNodes[0] == null){
        return;
      }
      //console.log(exceptNodes);
      let nodes = [];
      for(var i = 0 ;i < thisGraph.nodes.length; i++){
        let node = thisGraph.nodes[i];
        console.log(exceptNodes);
        let found = false;
        for(var j = 0 ;j < exceptNodes.length; j++){
          if(node.id == exceptNodes[j].id){
            found = true;
            break;
          }
        }
        if(!found){
          nodes.push(node);
        }
        found = true;
      }
      nodes.forEach(function(node){
        colorNode(node, getOldColor(node));
      });
    }

    GraphCreator.prototype.getCurrentPlayer = function(){
      return players[thisGraph.state.currentPlayer];
    }  

    GraphCreator.prototype.getNextPlayer = function(){
      return players[(thisGraph.state.currentPlayer + 1) % 2];
    }

    GraphCreator.prototype.updateSelectedAndPrevNode = function() {
      //TODO:: check for humans only.
      if(thisGraph.state.prevNode != null && thisGraph.state.prevNode.player != undefined){
        $("#attackerNode").text(thisGraph.state.prevNode.player == thisGraph.getCurrentPlayer() ? 
          thisGraph.state.prevNode.id : "-1");
      }
      if(thisGraph.state.selectedNode != null && thisGraph.state.selectedNode.player != undefined){
        $("#attackedNode").text(thisGraph.state.selectedNode.player == thisGraph.getNextPlayer() ? 
          thisGraph.state.selectedNode.id : "-1");
      }


      if(thisGraph.state.prevNode != null && thisGraph.state.prevNode.player != undefined){
        $("#moveFromNode").text(thisGraph.state.prevNode.player == thisGraph.getCurrentPlayer() ? 
          thisGraph.state.prevNode.id : "-1");
      }
      if(thisGraph.state.selectedNode != null && thisGraph.state.selectedNode.player != undefined){
        $("#moveToNode").text(thisGraph.state.selectedNode.player == thisGraph.getCurrentPlayer() ? 
          thisGraph.state.selectedNode.id : "-1");
      }

    }

    $(".hoverSpans").on('mouseover', function(){
      let nodeId = $(this).text();
      thisGraph.nodes.forEach(function(node, i){
        if(node.id == nodeId){
          colorNode(node, "pink");
        }
      });
    });

    $(".hoverSpans").on('mouseleave', function(){
      let nodeId = $(this).text();
      thisGraph.nodes.forEach(function(node, i){
        if(node.id == nodeId){
          colorNode(node, getOldColor(node));
        }
      });
    });

    function updateBonusUi(){
      $("#bonusVal").text(thisGraph.state.bonusVal);
      $("#bonusNode").text(thisGraph.state.bonusNode != undefined ? thisGraph.state.bonusNode.id : -1);
      //color bonus node with yellow.
      colorNode(thisGraph.state.bonusNode, "yellow");
      removeColorExcpetFrom([thisGraph.state.bonusNode]);
    }

    function updateMoveUi(){
      $("#movedToNode").text(thisGraph.state.moveToNode.id);
      $("#movedFromNode").text(thisGraph.state.moveFromNode.id);
      colorNode(thisGraph.state.moveToNode, "blue");
      colorNode(thisGraph.state.moveFromNode, "blue");
      removeColorExcpetFrom([thisGraph.state.moveToNode, thisGraph.state.moveFromNode]);
    }

    function updateAttackUi(){
      $("#attackedNode").text(thisGraph.state.attackedNode.id);
      $("#attackerNode").text(thisGraph.state.attackerNode.id);
      colorNode(thisGraph.state.attackedNode, "red");
      colorNode(thisGraph.state.attackerNode, "red");
      removeColorExcpetFrom([thisGraph.state.attackedNode, thisGraph.state.attackerNode]);
    }

    //some events to handle human agent inputs.
    $("#addBonus").click(function(){
      thisGraph.state.bonusNode = thisGraph.state.selectedNode;
      updateBonusUi();

      /*if(thisGraph.state.selectedNode == null){
        return;
      }
      if(thisGraph.state.bonusNode != null){
        if(thisGraph.state.selectedNode.id == thisGraph.state.bonusNode.id){
          return;
        }
      }
      thisGraph.state.selectedNode.title = (thisGraph.state.bonusVal + getArmy(thisGraph.state.selectedNode)).toString();
      thisGraph.nodes.forEach(function(node){
        if(node.id == thisGraph.state.selectedNode.id){
          node.title = thisGraph.state.selectedNode.title;
        }
        //remove bonus if wrongly given to a prev node.(user changed his mind.)
        if(thisGraph.state.bonusNode != null && node.id == thisGraph.state.bonusNode.id){
          node.title = (getArmy(node) - thisGraph.state.bonusVal).toString();
        }
      });
      thisGraph.state.bonusNode = thisGraph.state.selectedNode;
      thisGraph.updateGraph();
      updateBonusUi();*/
    });

    function moveSuccess(){
      thisGraph.state.selectedNode.title = (army + getArmy(thisGraph.state.selectedNode)).toString();
      thisGraph.state.prevNode.title = (getArmy(thisGraph.state.prevNode) - army).toString();
      thisGraph.nodes.forEach(function(node){
        if(node.id == thisGraph.state.selectedNode.id) {
          node.title = thisGraph.state.selectedNode.title;
        }
      });
      thisGraph.nodes.forEach(function(node){
        if(node.id == thisGraph.state.prevNode.id) {
          node.title = thisGraph.state.prevNode.title;
        }
      });
      updateMoveUi();
      thisGraph.updateGraph();
    }

    function moveFailure(){
      thisGraph.state.moveToNode = null;
      thisGraph.state.moveFromNode = null;
      thisGraph.state.movedArmies = -1;  
      $("#movedToNode").text(-1);
      $("#movedFromNode").text(-1); 
    }

    $("#addMove").click(function() {
      let army = Number($("#armyVal").val());
      thisGraph.state.moveToNode = thisGraph.state.selectedNode;
      thisGraph.state.moveFromNode = thisGraph.state.prevNode;
      thisGraph.state.movedArmies = army;
      updateMoveUi();
      //handleTurn(moveSuccess, moveFailure);
    });

    function attackSuccess(){
      thisGraph.state.selectedNode.title = (army + getArmy(thisGraph.state.selectedNode)).toString();
      thisGraph.state.prevNode.title = (getArmy(thisGraph.state.prevNode) - army).toString();
      thisGraph.nodes.forEach(function(node) {
        if(node.id == thisGraph.state.selectedNode.id) {
          node.title = thisGraph.state.selectedNode.title;
        }
      });
      thisGraph.nodes.forEach(function(node){
        if(node.id == thisGraph.state.prevNode.id){
          node.title = thisGraph.state.prevNode.title;
        }
      });
      thisGraph.updateGraph();
      updateMoveUi();
    }

    function attackFailure(){
      thisGraph.state.attackedNode = null;
      thisGraph.state.attackerNode = null;
      thisGraph.state.attackedNodeArmies = -1;
      $("#attackedFromNode").text(-1);
      $("#attackedToNode").text(-1);

    }

    $("#addAttack").click(function() {
      let army = Number($("#attackedArmyVal").val());
      thisGraph.state.attackedNode = thisGraph.state.selectedNode;
      thisGraph.state.attackerNode = thisGraph.state.prevNode;
      thisGraph.state.attackedNodeArmies = army;
      updateAttackUi();
      //handleTurn(attackSuccess, attackFailure);
    });

    $("#doAction").click(function() {
      handleTurn();
    });

    $("#p1Algo").on("change", function(){
      thisGraph.state.algo1 = $(this).find("option:selected").text()
    });

    $("#p2Algo").on("change", function(){
      thisGraph.state.algo2 = $(this).find("option:selected").text()
    });
  
  };



  GraphCreator.prototype.setIdCt = function(idct){
    this.idct = idct;
  };

  GraphCreator.prototype.consts =  {
    selectedClass: "selected",
    connectClass: "connect-node",
    circleGClass: "conceptG",
    graphClass: "graph",
    activeEditId: "active-editing",
    BACKSPACE_KEY: 8,
    DELETE_KEY: 46,
    ENTER_KEY: 13,
    nodeRadius: 50,
    HELP:27,
  };

  /* PROTOTYPE FUNCTIONS */

  GraphCreator.prototype.dragmove = function(d) {
    var thisGraph = this;
    if (thisGraph.state.shiftNodeDrag){
      thisGraph.dragLine.attr('d', 'M' + d.x + ',' + d.y + 'L' + d3.mouse(thisGraph.svgG.node())[0] + ',' + d3.mouse(this.svgG.node())[1]);
    } else{
      d.x += d3.event.dx;
      d.y +=  d3.event.dy;
      thisGraph.updateGraph();
    }
  };

  GraphCreator.prototype.deleteGraph = function(skipPrompt){
    var thisGraph = this,
        doDelete = true;
    if (!skipPrompt){
      doDelete = window.confirm("Press OK to delete this graph");
    }
    if(doDelete){
      thisGraph.nodes = [];
      thisGraph.edges = [];
      thisGraph.updateGraph();
    }
  };

  /* select all text in element: taken from http://stackoverflow.com/questions/6139107/programatically-select-text-in-a-contenteditable-html-element */
  GraphCreator.prototype.selectElementContents = function(el) {
    var range = document.createRange();
    range.selectNodeContents(el);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  };


  /* insert svg line breaks: taken from http://stackoverflow.com/questions/13241475/how-do-i-include-newlines-in-labels-in-d3-charts */
  GraphCreator.prototype.insertTitleLinebreaks = function (gEl, title) {
    var words = title.split(/\s+/g),
        nwords = words.length;
    var el = gEl.append("text")
          .attr("text-anchor","middle")
          .attr("dy", "-" + (nwords-1)*7.5);

    for (var i = 0; i < words.length; i++) {
      var tspan = el.append('tspan').text(words[i]);
      if (i > 0)
        tspan.attr('x', 0).attr('dy', '15');
    }
  };


  // remove edges associated with a node
  GraphCreator.prototype.spliceLinksForNode = function(node) {
    var thisGraph = this,
        toSplice = thisGraph.edges.filter(function(l) {
      return (l.source === node || l.target === node);
    });
    toSplice.map(function(l) {
      thisGraph.edges.splice(thisGraph.edges.indexOf(l), 1);
    });
  };

  GraphCreator.prototype.replaceSelectEdge = function(d3Path, edgeData){
    var thisGraph = this;
    d3Path.classed(thisGraph.consts.selectedClass, true);
    if (thisGraph.state.selectedEdge){
      thisGraph.removeSelectFromEdge();
    }
    thisGraph.state.selectedEdge = edgeData;
  };

  GraphCreator.prototype.replaceSelectNode = function(d3Node, nodeData){
    var thisGraph = this;
    
    let selectedNode = thisGraph.state.selectedNode;
    if(selectedNode){
      thisGraph.state.prevNode = thisGraph.state.selectedNode;
      thisGraph.state.selectedNode = nodeData;
    } else if(selectedNode == null){
      //if no selected so far then prev = cur.
      thisGraph.state.selectedNode = nodeData;
      thisGraph.state.prevNode = nodeData;
    }
    thisGraph.removeSelectFromNode();
    d3Node.classed(this.consts.selectedClass, true);
    //update UI with new nodes.
    thisGraph.updateSelectedAndPrevNode();
  };

  GraphCreator.prototype.removeSelectFromNode = function(){
    var thisGraph = this;
    thisGraph.circles.filter(function(cd){
      if(thisGraph.state.selectedNode == null){
        return true;
      }
      return cd.id !== thisGraph.state.selectedNode.id;
    }).classed(thisGraph.consts.selectedClass, false);
    //thisGraph.state.selectedNode = null;
  };

  GraphCreator.prototype.removeSelectFromEdge = function(){
    var thisGraph = this;
    thisGraph.paths.filter(function(cd){
      return cd === thisGraph.state.selectedEdge;
    }).classed(thisGraph.consts.selectedClass, false);
    thisGraph.state.selectedEdge = null;
  };

  GraphCreator.prototype.pathMouseDown = function(d3path, d){
    var thisGraph = this,
        state = thisGraph.state;
    d3.event.stopPropagation();
    state.mouseDownLink = d;
    if (state.selectedNode){
      thisGraph.removeSelectFromNode();
    }

    var prevEdge = state.selectedEdge;
    if (!prevEdge || prevEdge !== d){
      thisGraph.replaceSelectEdge(d3path, d);
    } else{
      thisGraph.removeSelectFromEdge();
    }
  };

  // mousedown on node
  GraphCreator.prototype.circleMouseDown = function(d3node, d){
    var thisGraph = this,
        state = thisGraph.state;
    d3.event.stopPropagation();
    state.mouseDownNode = d;
    if (d3.event.shiftKey){
      state.shiftNodeDrag = d3.event.shiftKey;
      // reposition dragged directed edge
      thisGraph.dragLine.classed('hidden', false)
        .attr('d', 'M' + d.x + ',' + d.y + 'L' + d.x + ',' + d.y);
      return;
    }
  };

  /* place editable text on node in place of svg text */
  GraphCreator.prototype.changeTextOfNode = function(d3node, d){
    var thisGraph= this,
        consts = thisGraph.consts,
        htmlEl = d3node.node();
    d3node.selectAll("text").remove();
    var nodeBCR = htmlEl.getBoundingClientRect(),
        curScale = nodeBCR.width/consts.nodeRadius,
        placePad  =  5*curScale,
        useHW = curScale > 1 ? nodeBCR.width*0.71 : consts.nodeRadius*1.42;
    // replace with editableconent text
    var d3txt = thisGraph.svg.selectAll("foreignObject")
          .data([d])
          .enter()
          .append("foreignObject")
          .attr("x", nodeBCR.left + placePad )
          .attr("y", nodeBCR.top + placePad)
          .attr("height", 2*useHW)
          .attr("width", useHW)
          .append("xhtml:p")
          .attr("id", consts.activeEditId)
          .attr("contentEditable", "true")
          .text(d.title)
          .on("mousedown", function(d){
            d3.event.stopPropagation();
          })
          .on("keydown", function(d){
            d3.event.stopPropagation();
            if (d3.event.keyCode == consts.ENTER_KEY && !d3.event.shiftKey){
              this.blur();
            }
          })
          .on("blur", function(d){
            d.title = this.textContent;
            thisGraph.insertTitleLinebreaks(d3node, d.title);
            d3.select(this.parentElement).remove();
          });
    return d3txt;
  };

  // mouseup on nodes
  GraphCreator.prototype.circleMouseUp = function(d3node, d){
    var thisGraph = this,
        state = thisGraph.state,
        consts = thisGraph.consts;
    // reset the states
    state.shiftNodeDrag = false;
    d3node.classed(consts.connectClass, false);

    var mouseDownNode = state.mouseDownNode;

    if (!mouseDownNode) return;

    thisGraph.dragLine.classed("hidden", true);

    if (mouseDownNode !== d){
      // we're in a different node: create new edge for mousedown edge and add to graph
      var newEdge = {source: mouseDownNode, target: d};
      var filtRes = thisGraph.paths.filter(function(d){
        if (d.source === newEdge.target && d.target === newEdge.source){
          thisGraph.edges.splice(thisGraph.edges.indexOf(d), 1);
        }
        return d.source === newEdge.source && d.target === newEdge.target;
      });
      if (!filtRes[0].length){
        thisGraph.edges.push(newEdge);
        thisGraph.updateGraph();
      }
    } else{
      // we're in the same node
      if (state.justDragged) {
        // dragged, not clicked
        state.justDragged = false;
      } else{
        // clicked, not dragged
        if (d3.event.shiftKey){
          // shift-clicked node: edit text content
          var d3txt = thisGraph.changeTextOfNode(d3node, d);
          var txtNode = d3txt.node();
          thisGraph.selectElementContents(txtNode);
          txtNode.focus();
          //$("#nodeVal").val($(txtNode).text());
        } else{
          if (state.selectedEdge){
            thisGraph.removeSelectFromEdge();
          }
          var prevNode = state.selectedNode;
          if (!prevNode || prevNode.id !== d.id){
            thisGraph.replaceSelectNode(d3node, d);
          } else {
            thisGraph.removeSelectFromNode();
          }
        }
      }
    }
    state.mouseDownNode = null;
    return;

  }; // end of circles mouseup

  // mousedown on main svg
  GraphCreator.prototype.svgMouseDown = function(){
    this.state.graphMouseDown = true;
    this.state.selectedNode = null;
    this.removeSelectFromNode()
    //thisGraph.removeSelectFromNode();
    //thisGraph.updateGraph();
  };

  // mouseup on main svg
  GraphCreator.prototype.svgMouseUp = function(){
    var thisGraph = this,
        state = thisGraph.state;
    if (state.justScaleTransGraph) {
      // dragged not clicked
      state.justScaleTransGraph = false;
    } else if (state.graphMouseDown && d3.event.shiftKey){
      // clicked not dragged from svg
      var xycoords = d3.mouse(thisGraph.svgG.node()),
          d = {id: thisGraph.idct++, title: consts.defaultTitle, x: xycoords[0], y: xycoords[1]};
      thisGraph.nodes.push(d);
      thisGraph.updateGraph();
      // make title of text immediently editable
      var d3txt = thisGraph.changeTextOfNode(thisGraph.circles.filter(function(dval){
        return dval.id === d.id;
      }), d),
          txtNode = d3txt.node();
      thisGraph.selectElementContents(txtNode);
      txtNode.focus();
      //add node data to textbox.
      //$("#nodeVal").val($(txtNode).text());
    } else if (state.shiftNodeDrag){
      // dragged from node
      state.shiftNodeDrag = false;
      thisGraph.dragLine.classed("hidden", true);
    }
    state.graphMouseDown = false;
  };

  // keydown on main svg
  GraphCreator.prototype.svgKeyDown = function() {
    var thisGraph = this,
        state = thisGraph.state,
        consts = thisGraph.consts;
    // make sure repeated key presses don't register for each keydown
    if(state.lastKeyDown !== -1) return;

    state.lastKeyDown = d3.event.keyCode;
    var selectedNode = state.selectedNode,
        selectedEdge = state.selectedEdge;
    switch(d3.event.keyCode) {
    //case consts.BACKSPACE_KEY:
    case consts.DELETE_KEY:
      d3.event.preventDefault();
      if (selectedNode){
        thisGraph.nodes.splice(thisGraph.nodes.indexOf(selectedNode), 1);
        thisGraph.spliceLinksForNode(selectedNode);
        state.selectedNode = null;
        thisGraph.updateGraph();
      } else if (selectedEdge){
        thisGraph.edges.splice(thisGraph.edges.indexOf(selectedEdge), 1);
        state.selectedEdge = null;
        thisGraph.updateGraph();
      }
      break;
    }
  };

  GraphCreator.prototype.svgKeyUp = function() {
    this.state.lastKeyDown = -1;
  };

  // call to propagate changes to graph
  GraphCreator.prototype.updateGraph = function(){
    var thisGraph = this,
        consts = thisGraph.consts,
        state = thisGraph.state;

    thisGraph.paths = thisGraph.paths.data(thisGraph.edges, function(d){
      return String(d.source.id) + "+" + String(d.target.id);
    });
    var paths = thisGraph.paths;
    // update existing paths
    //.style('marker-end', 'url(#end-arrow)')
    paths.classed(consts.selectedClass, function(d){
        return d === state.selectedEdge;
      })
      .attr("d", function(d){
        return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;
      });

    // add new paths
    paths.enter()
      .append("path")
      //.style('marker-end','url(#end-arrow)')
      .classed("link", true)
      .attr("d", function(d){
        return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;
      })
      .on("mousedown", function(d){
        thisGraph.pathMouseDown.call(thisGraph, d3.select(this), d);
        }
      )
      .on("mouseup", function(d){
        state.mouseDownLink = null;
      });

    // remove old links
    paths.exit().remove();

    // update existing nodes
    thisGraph.circles = thisGraph.circles.data(thisGraph.nodes, function(d){ return d.id;});
    thisGraph.circles.attr("transform", function(d){return "translate(" + d.x + "," + d.y + ")";});
    // add new nodes
    var newGs= thisGraph.circles.enter()
          .append("g");

    newGs.classed(consts.circleGClass, true)
      .attr("transform", function(d){return "translate(" + d.x + "," + d.y + ")";})
      .on("mouseover", function(d){
        if (state.shiftNodeDrag){
          d3.select(this).classed(consts.connectClass, true);
        }
      })
      .on("mouseout", function(d){
        d3.select(this).classed(consts.connectClass, false);
      })
      .on("mousedown", function(d){
        thisGraph.circleMouseDown.call(thisGraph, d3.select(this), d);
      })
      .on("mouseup", function(d){
        thisGraph.circleMouseUp.call(thisGraph, d3.select(this), d);
      })
      .call(thisGraph.drag);

    newGs.append("circle")
      .attr("r", String(consts.nodeRadius));

    newGs.each(function(d){
      thisGraph.insertTitleLinebreaks(d3.select(this), d.title);
    });

    // remove old nodes
    thisGraph.circles.exit().remove();
    //update colors and text.
    thisGraph.circles[0].parentNode.childNodes.forEach(function(g, i){
      //if nodes exists.
      if(g !== undefined){
        //has color.
        let node = thisGraph.nodes[i];
        if(thisGraph.nodes[i].player !== undefined){
          $(g.childNodes[0]).css("fill", node.player == "Player 1" ? "#d39e00" : "#299a43");
        }
        $(g.childNodes[1]).text(node.title);

        $(g).attr('data-toggle', 'tooltip');
        $(g).attr('data-placement', 'top');
        $(g).attr('title', "Node id: " + node.id);
      }
    });
    $('[data-toggle="tooltip"]').tooltip();

  };

  GraphCreator.prototype.zoomed = function(){
    this.state.justScaleTransGraph = true;
    d3.select("." + this.consts.graphClass)
      .attr("transform", "translate(" + d3.event.translate + ") scale(" + d3.event.scale + ")");
  };

  GraphCreator.prototype.updateWindow = function(svg){
    var docEl = document.documentElement,
        bodyEl = document.getElementsByTagName('body')[0];
        var x = docEl.clientWidth,
        y =  docEl.clientHeight;
    svg.attr("width", "100%").attr("height", y);
  };

  function intitializeUi(){
    $("#bonusVal").text(consts.defaultUnkown);
    $("#bonusNode").text(consts.defaultUnkown);
    $("#attackerNode").text(consts.defaultUnkown);
    $("#attackedNode").text(consts.defaultUnkown);
    $("#moveFromNode").text(consts.defaultUnkown);
    $("#moveToNode").text(consts.defaultUnkown);
    $("#attackedNode").text(consts.defaultUnkown);
  }

  /**** MAIN ****/
  var closed = true;
  document.addEventListener('keydown', function(e){
    //escape key on keyboard.
    if(e.keyCode == 27){
      if(closed){
        $('#helpModal').modal("show");
        closed = false;
      }else{
        $('#helpModal').modal("hide");
        closed = true;
      }
    }
  });

  // warn the user when leaving
  window.onbeforeunload = function(){
    return "Make sure to save your graph locally before leaving :-)";
  };

  var docEl = document.documentElement,
      bodyEl = document.getElementsByTagName('body')[0];

  var width = docEl.clientWidth,
      height =  docEl.clientHeight;

  var xLoc = width/2 - 25,
      yLoc = 100;

  // initial node data
  var nodes = [];
  var edges = [];
  var partitions = [] || document.getElementById('partitions');

  /** MAIN SVG **/
  var svg = d3.select(settings.appendElSpec).append("svg")
        .attr("width", "100%")
        .attr("height", height);
  var graph = new GraphCreator(svg, nodes, edges, partitions);
      graph.setIdCt(0);

  document.getElementById("root").style.maxWidth = "100%";
  graph.updateGraph();
  intitializeUi();
  $(".alert").alert()
  //enable tool tip everywhere.
  $('[data-toggle="tooltip"]').tooltip()
})(window.d3, window.saveAs, window.Blob);
