#!/usr/bin/python3
#coding:utf8
# mailliao@163.com


# map有两层，一层里定义polygon、line的样式，用于画各个国家边界线
# 另一层里只定义了线的样式，用于画两国公共边界，红色的
import mapnik
# 第一部分，创建地图，指定地图底色
m = mapnik.Map(500,1000)
m.background = mapnik.Color('#8080a0')

# 第二部分，画地图，此时是全世界所有国家均有
# 定义画显示出的所有国家的边界线，黑色的边界线
# 也定义各个国家内部填色steelblue
# 这些放在layer层
s = mapnik.Style()
r = mapnik.Rule()
polygon_symbolizer = mapnik.PolygonSymbolizer()
polygon_symbolizer.fill = mapnik.Color('steelblue')
r.symbols.append(polygon_symbolizer)

line_symbolizer = mapnik.LineSymbolizer()
line_symbolizer.stroke = mapnik.Color('black')
line_symbolizer.stroke_width = 0.5
r.symbols.append(line_symbolizer)
s.rules.append(r)
m.append_style('My Style',s)
# 全世界所有国家的shp文件
ds = mapnik.Shapefile(file='./tm/TM_WORLD_BORDERS-0.3.shp')
layer = mapnik.Layer('world')
layer.datasource = ds
layer.styles.append('My Style')
m.layers.append(layer)

# 第三部分，画某两国公共边界 
# 读取两个国家的公共边界线的shp文件
ds1 = mapnik.Shapefile(file='common-border/border.shp')
s1 = mapnik.Style()
r1 = mapnik.Rule()
line_symbolizer = mapnik.LineSymbolizer()
# 为画出公共边界线，设定特定颜色为红色
line_symbolizer.stroke = mapnik.Color('red')
line_symbolizer.stroke_width = 1.3
r1.symbols.append(line_symbolizer)
s1.rules.append(r1)
m.append_style('My Style1',s1)

# layer1层在layer层上，这一层只画了一条线，即两国公共边界
layer1 = mapnik.Layer('thmm')
layer1.datasource = ds1
layer1.styles.append('My Style1')
m.layers.append(layer1)

# 第四部分，渲染出地图
#m.zoom_all()
# (92, 5, 106, 29)是两个国家的最大、最小经纬度，即包络矩形
m.zoom_to_box(mapnik.Box2d(92, 5, 106, 29))
mapnik.render_to_file(m,'world.png', 'png')
print("rendered image to 'world.png'")
