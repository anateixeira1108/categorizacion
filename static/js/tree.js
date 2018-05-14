
function Tree(id, name, content, state, type) {

    var cached_this = this;
    cached_this.id = id;
    cached_this.name = name;
    cached_this.state = state;
    cached_this.type = type;
    cached_this.content = content;
    cached_this.children = [];
    cached_this.parent = undefined;

    cached_this.setParentNode = function(node) {
        if( cached_this !== undefined ){
            cached_this.parent = node;
        }
    }

    cached_this.getParentNode = function() {
        return cached_this !== undefined? cached_this.parent : undefined;
    }

    cached_this.addChild = function(node) {
        if( cached_this !== undefined ){
            node.setParentNode(cached_this);
            cached_this.children.push(node);
        }
    }

    cached_this.getChildren = function() {
        return cached_this !== undefined? cached_this.children : undefined;
    }

    cached_this.removeChildren = function() {
        if(cached_this!== undefined){                  
            delete cached_this.id;
            delete cached_this.name;
            delete cached_this.state;
            delete cached_this.content;
            delete cached_this.children;
            delete cached_this.parent;
            delete cached_this.type;
            delete cached_this;
        }
    }

    cached_this.render = function(ignore_data){
        if( cached_this !== undefined && cached_this.children !== undefined ){
            var data = ['data has been ignored'];
            if (ignore_data !== undefined){
                data = [];
                for ( var i =0; i<cached_this.children.length; ++i){
                    data.push(cached_this.children[i].render(false));
                }
            }
            return {
                'id': cached_this.id, 
                'name': cached_this.name, 
                'state': cached_this.state,
                'content': cached_this.content,
                'children': data,
                'parent': cached_this.parent,
                'type': cached_this.type
            }
        }   
    }

    cached_this.addChildByIndex = function(id, type, node){
        if( cached_this !== undefined ){
            if( cached_this.id === id && cached_this.type === type )
            {
                cached_this.addChild(node);
            }else{
                for ( var i =0; i<cached_this.children.length; ++i ){
                    cached_this.children[i].addChildByIndex( id, type, node );
                }
            }
        }
    }

    cached_this.deleteByIndex = function( id, type )
    {
        if(cached_this !== undefined ){
            if( cached_this.id === id && cached_this.type === type )
            {
                if(cached_this.getParentNode() !== undefined ){
                    cached_this.removeChildren();
                }else{
                    cached_this.removeChildren();
                    delete cached_this.id;
                    delete cached_this.name;
                    delete cached_this.state;
                    delete cached_this.content;
                    delete cached_this.children;
                    delete cached_this.parent;
                    delete cached_this.type;
                    delete cached_this;
                }
            }else{
                for ( var i =0;  i< cached_this.children.length; ++i ){
                    cached_this.children[i].deleteByIndex( id, type );
                }
            }
        }
    }

    cached_this.load = function(obj, pid, ptype){        
        if( cached_this.id === undefined )
        {            
            cached_this.id = obj[0].id;
            cached_this.name = obj[0].name;
            cached_this.state = obj[0].state;
            cached_this.type = obj[0].type;            
            cached_this.load (object[0].children, cached_this.id, cached_this.type);
        }else{            
            for (var i = 0; i < obj.length; ++i) {           
                cached_this.addChildByIndex(
                    pid, 
                    ptype, 
                    new Tree(obj[i].id, obj[i].name, obj[i].content, obj[i].state, obj[i].type))                
                cached_this.load( obj[i].children, obj[i].id, obj[i].type );
            }
        }
    }
}
