#!/usr/bin/python3
import mapnik
m = mapnik.Map(500,1000)
m.background = mapnik.Color('#8080a0')
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

ds = mapnik.Shapefile(file='./tm/TM_WORLD_BORDERS-0.3.shp')
layer = mapnik.Layer('world')
layer.datasource = ds
layer.styles.append('My Style')
m.layers.append(layer)


ds1 = mapnik.Shapefile(file='common-border/border.shp')
s1 = mapnik.Style()
r1 = mapnik.Rule()
line_symbolizer = mapnik.LineSymbolizer()
line_symbolizer.stroke = mapnik.Color('red')
line_symbolizer.stroke_width = 1.3

r1.symbols.append(line_symbolizer)
s1.rules.append(r1)
m.append_style('My Style1',s1)

layer1 = mapnik.Layer('thmm')
layer1.datasource = ds1
layer1.styles.append('My Style1')
m.layers.append(layer1)
#m.zoom_all()
m.zoom_to_box(mapnik.Box2d(92, 5, 106, 29))
mapnik.render_to_file(m,'world.png', 'png')
print("rendered image to 'world.png'")
