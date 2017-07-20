#!/usr/bin/python
#coding:utf-8
# mailliao@163.com
# 数据从http://thematicmapping.org/downloads/world_borders.php下载
# calcCommonBorders.py
# 如何创建一个shp文件，本程序和p55_5.py程序
import os, os.path, shutil
from osgeo import ogr, osr
import shapely.wkt
# 读取数据源
shapefile = ogr.Open("./tm/TM_WORLD_BORDERS-0.3.shp")
# 读取第0层数据，获得访问句柄，类似c里的文件句柄
layer = shapefile.GetLayer(0)
thailand = None
myanmar = None
p = layer.GetLayerDefn()
feature = layer.GetFeature(0)
for i in range(0, p.GetFieldCount()):
	print(i, p.GetFieldDefn(i).GetName())#, feature.GetFieldAsString(i)


for i in range(feature.GetFieldCount()):
	print("field def", feature.GetFieldDefnRef(i), feature.GetFieldAsString(i))
	
for i in range(layer.GetFeatureCount()):
	#获得第n条记录
	feature = layer.GetFeature(i)
	
	# 获取th和mm两个国家的polygon多边形曲线数据,通过GetGeometryRef方法
	# th：Thailand
	# mm: Myanmar
	if feature.GetField("ISO2") == "TH":
		geometry = feature.GetGeometryRef()
		minLong,maxLong,minLat,maxLat = geometry.GetEnvelope()
		print("TH", minLat, maxLat, minLong, maxLong)
		# 转换polygon数据为 Shapely geometry objects数据
		# 将polygon数据变成LineString数据，即多变曲线变成多个(条)线
		# ExportToWkt() 函数可以将地理信息数据polygon、line(一系列数据)等转为纯文本“字符串”
		# 数字=>文本字符串
		# line = shapely.wkt.loads('LINESTRING (380 60, 360 130, 230 350, 140 410)')
		thailand = shapely.wkt.loads(geometry.ExportToWkt())
		#print i, "geometry", geometry
	elif feature.GetField("ISO2") == "MM":
		geometry = feature.GetGeometryRef()
		minLong,maxLong,minLat,maxLat = geometry.GetEnvelope()
		print("MM", minLat, maxLat, minLong, maxLong)
		myanmar = shapely.wkt.loads(geometry.ExportToWkt())
		#print i, "geometry", geometry
#获得公共边界数据信息,共享的线条LineString
commonBorder = thailand.intersection(myanmar)
#创建保存数据的零时存储目录
if os.path.exists("common-border"):
	shutil.rmtree("common-border")
os.mkdir("common-border")









# 将公共边界线，写入到border.shp文件里去
# 0设置shp文件的数据模型
spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS('WGS84')
driver = ogr.GetDriverByName("ESRI Shapefile")
# 1存储文件名
dstPath = os.path.join("common-border", "border.shp")
#print(dstPath)
# 创建shp文件
dstFile = driver.CreateDataSource(dstPath)
# 2创建层
dstLayer = dstFile.CreateLayer("layer", spatialReference)
# 共享边界线地理信息数据
wkt = shapely.wkt.dumps(commonBorder)

# 3创建feature记录
feature = ogr.Feature(dstLayer.GetLayerDefn())
# 给feature设置地理信息数据，这里没有给文件赋域信息。参看p55_5.py文件
feature.SetGeometry(ogr.CreateGeometryFromWkt(wkt))
# 创建feature记录，只有一条记录
dstLayer.CreateFeature(feature)
print(ogr.CreateGeometryFromWkt(wkt))







