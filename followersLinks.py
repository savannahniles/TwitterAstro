import json
import io

accountNames = ["sannabh", "ottolinguini", "jgrayjgray"]
group = "friends"

#new file for the big json
NODES_FILE = group + '-nodes.json'
f_nodes = io.open(NODES_FILE, 'w', encoding='utf8')
LINKS_FILE = group + '-links.json'
f_links = io.open(LINKS_FILE, 'w', encoding='utf8')

nodes = []
links = []

class Node:

	def __init__(self, name, screen_name, group, followers_count, followers): #makes 1 call to users
		self.name = name
		self.screen_name = screen_name
		self.group = group
		self.followers_count = followers_count
		self.followers = followers

class Link:
	
	def __init__(self, source, target, value): #makes 1 call to users
		self.source = source
		self.target = target
		self.value = value

#get nodes  first
for name in accountNames:
	json_data=open(name + '-followers.txt') #open file for that person
	data = json.load(json_data)
	node = Node(data["name"], data["screen_name"], group, data["followers_count"], data["followers"])
	nodes.append(node)
	# print node.jsonable()


#now do links:
#shit's already in memory

for i, source in enumerate(nodes):
	# print "CURRENT SOURCE IS", source, "AT CHARACTER", index 
    k = i+1
    for target in nodes[k:len(nodes)]:
    	if (source.followers) and (target.followers):
    		print "%s %s" % (source.name, target.name)
    		intersection = list(set(source.followers) & set(target.followers))
    		val = len(intersection)
    		# print val
    		if val > 0:
    			link = Link(source.screen_name, target.screen_name, val)
    			links.append(link)

def encode_link(link):
    if isinstance(link, Link):
        return link.__dict__
    return link

print unicode(json.dumps(links, default=encode_link))
f_links.write(unicode(json.dumps(links, default=encode_link)))

#go through and clear memory in each node

def encode_node(node):
    if isinstance(node, Node):
        return node.__dict__
    return node

for node in nodes:
	node.followers = None

# print unicode(json.dumps(nodes, default=encode_node))
f_nodes.write(unicode(json.dumps(nodes, default=encode_node)))


 # peopleNodes.each_with_index do |source, i| #iterate through each person
 # k = i+1
 #    peopleNodes[k...peopleNodes.count].each do |target| #might have to check that val...may be -1
 #      if (source.x != nil) & (target.x != nil)
 #          intersection = source.urls & target.urls
 #          val = intersection.count
 #          # puts "#{source.id} #{target.id} #{val} #{intersection}"
 #          if val > 0
 #            link = PersonLink.new(source.id, target.id, val)
 #            # link = PersonLink.new(source.id, target.id, val, intersection)
 #            peopleLinks.push(link)
 #          end
 #      end
 #    end
 # end







