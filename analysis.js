function doBlock(num){
    var b = eth.getBlock(num).hash
    debug.standardTraceBlockToFile(b,{
        "disableMemory": true, "disableStorage": true,
    })
    debug.standardTraceBlockToFile(b,{
        "disableMemory": true, "disableStorage": true,
        "overrides":{
            "yoloV2Block": 0
        }})
}

function doBlocks(start, end){
    for (var i = start; i <= end; i++){
            doBlock(i)
    }
}

//doBlocks(3321372,3321425)
