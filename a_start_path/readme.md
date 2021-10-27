# A* pathfinding visualization using python

## following the tutorial by Tech With Tim
## https://www.youtube.com/watch?v=JtiK0DOeI4A

### A* tries to find the shortest possible path between 2 points

### theory:
there are
- weighted edges
  - the weight determines how much distance/how hard it is to move along that path
- nodes
  - the points between the start and finish
- edges
  - in this case all the edges will have a weight of 1


A* will try to find the shortest path
- it is an informed algoritm so:
  - it won't bruteforce the paths
  - it won't considder the paths that are extremely long

- it has 3 scores:
  - h-score(n)
    - estimate distance from node n to end-node
    - doesn't use possible paths, just the absolute distance in "bird flight" 
  - G-score(n)
    - current shortest distance from start node (using paths) to current node
  - F-score(n)
    - F-score(n) = G-score(n) + H-score(n) 
    - this score is used to prioritize the further looking into notes
- if you haven't calculated the node then the F,G and H-scores are all infinity
- in the open-set you have all the possible nodes with the same F-score (these are the nodes that we will calculate the neighbours of next)
  - in the beginning it is always the startnode with a score of 0
- when you take the endnode from the open-set you end the algoritm