from imposm.parser import OSMParser
from couchdbkit import Server

class p:
	def __init__(self):
		server = Server()
		self.db=server.get_or_create_db("b")
		self.i=0
		self.parser=OSMParser(nodes_callback=self.coord, ways_callback=self.way, relations_callback=self.rel, coords_callback=self.coord)
	def parse(self,x):
		self.parser.parse(x)
	def coord(self,c):
		out=dict()
		for osm_id,lat,lng in c:
			out["type"]="coord"
			out["_id"]=str(osm_id)
			out["geometry"]={"type":"Point","coordinates":lng}
			self.db["c"+str(osm_id)]=out
		self.i=self.i+1
		print "cached a coord totoal now "+str(self.i)
	def node(self,n):
		out=dict()
		for osm_id,tags,coord in n:
			c=[coord[0],coord[1]]
			out["type"]="node"
			out["_id"]=str(osm_id)
			out["geometry"]={"type":"Point","coordinates":c}
			for k in tags:
				if k !="type" and k!="_id"and k!="geometry":
					out[k]=tags[k]
			self.db[str(osm_id)]=out
		self.i=self.i+1
		print "cached a node totoal now "+str(self.i)
	def way(self,w):
		out=dict()
		for osm_id,tags,mem in w:
			out["type"]="way"
			out["_id"]=str(osm_id)
			out["members"]=mem
			for k in tags:
				if k !="type" and k!="_id"and k!="members":
					out[k]=tags[k]
			self.db[str(osm_id)]=out
		self.i=self.i+1
		print "cached a way totoal now "+str(self.i)
	def rel(self,r):
		out=dict()
		for osm_id,tags,mem in r:
			out["type"]="relation"
			out["_id"]=str(osm_id)
			out["members"]=mem
			for k in tags:
				if k !="type" and k!="_id"and k!="members":
					out[k]=tags[k]
			self.db[str(osm_id)]=out
		self.i=self.i+1
		print "cached a rel totoal now "+str(self.i)
	def clean(self):
		for k in self.nodes:
			if self.coords.has_key(k):
				del self.coords[k]
def cache(x):
	c=p()
	c.parse(x)
		

