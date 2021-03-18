/*
 * 所有的环绕点都是从左上角开始顺时针排布
 * https://api.map.baidu.com/lbsapi/getpoint/index.html
 */

// 东区生活区
var polygon_2 = new BMap.Polygon([
    new BMap.Point(121.438157,31.033921),   
    new BMap.Point(121.440978,31.034818),
    new BMap.Point(121.441867,31.03283),    //学森路-思源北路
    new BMap.Point(121.442604,31.031213),   //学森路-宣怀大道
    new BMap.Point(121.443107,31.030084),   //东中院的左上角
    new BMap.Point(121.443296,31.029314),
    new BMap.Point(121.443224,31.0288),
    new BMap.Point(121.443888,31.028521),
    new BMap.Point(121.444513,31.027148),
    new BMap.Point(121.441337,31.026193),
], {strokeColor:"green", strokeWeight:2, strokeOpacity:0.5, fillColor:"green", fillOpacity:0.1});  //创建多边形



// 东区教学楼
var polygon_1 = new BMap.Polygon([
    new BMap.Point(121.442595,31.031213),   // 宣怀大道-学森路
    new BMap.Point(121.443718,31.031608),
    new BMap.Point(121.445537,31.027446),
    new BMap.Point(121.444513,31.027156),
    new BMap.Point(121.443866,31.028514),
    new BMap.Point(121.443228,31.028811),
    new BMap.Point(121.443264,31.029438),
    new BMap.Point(121.443084,31.030065),
], {strokeColor:"green", strokeWeight:2, strokeOpacity:0.5, fillColor:"green", fillOpacity:0.1});  //创建多边形

// 东上院
var polygon_1_1 = new BMap.Polygon([
    new BMap.Point(121.443888,31.028521), 
    new BMap.Point(121.444975,31.028831),
    new BMap.Point(121.445532,31.027473),
    new BMap.Point(121.444513,31.027148),
], {strokeColor:"green", strokeWeight:2, strokeOpacity:0.5, fillColor:"green", fillOpacity:0.1});

// 东中院
var polygon_1_2 = new BMap.Polygon([
    new BMap.Point(121.443107,31.030084), 
    new BMap.Point(121.444059,31.030421),
    new BMap.Point(121.444046,31.030622),
    new BMap.Point(121.444104,31.03073),
    new BMap.Point(121.444975,31.028831),
    new BMap.Point(121.443888,31.028521),
    new BMap.Point(121.443224,31.0288),
    new BMap.Point(121.443296,31.029314),
], {strokeColor:"green", strokeWeight:2, strokeOpacity:0.5, fillColor:"green", fillOpacity:0.1});

// 东下院
var polygon_1_3 = new BMap.Polygon([
    new BMap.Point(121.442595,31.031213),  
    new BMap.Point(121.443718,31.031608), 
    new BMap.Point(121.44374,31.031608),
    new BMap.Point(121.444104,31.03073),
    new BMap.Point(121.444046,31.030622),
    new BMap.Point(121.444059,31.030421),
    new BMap.Point(121.443107,31.030084),
], {strokeColor:"green", strokeWeight:2, strokeOpacity:0.5, fillColor:"green", fillOpacity:0.1});

var areaDic = {
    "东区教学楼": polygon_1,
    "东上院": polygon_1_1,
    "东中院": polygon_1_2,
    "东下院": polygon_1_3,
    "东区生活区": polygon_2,
}

var subAreaDic = {
    "东区教学楼": ["东上院", "东中院", "东下院"],
    "东上院": [],
    "东中院": [],
    "东下院": [],
    "东区生活区": [],
}

var parentAreaDic = {
    "东区教学楼": "",
    "东上院": "东区教学楼",
    "东中院": "东区教学楼",
    "东下院": "东区教学楼",
    "东区生活区": "",
}

function getPolygonByName(areaName){
    return areaDic[areaName];
}

function getSubAreaByName(areaName){
    return subAreaDic[areaName];
}

function getParentAreaByName(areaName){
    return parentAreaDic[areaName];
}

 function setPolygonColor(areaName, colorName){
    areaDic[areaName].setFillColor(colorName);
    areaDic[areaName].setStrokeColor(colorName);
}

// 将传入的函数fun在所有的区域多边形上调用
// 传递进来的函数需要接受一个多边形对象和一个对应的区域名字作为参数
function iteratePolygon(fun){
    for(var key in areaDic){
        fun(areaDic[key], key);
    }
}