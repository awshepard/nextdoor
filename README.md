# Next Door, Skip Two

This is an old solitaire game my father taught me.  He has won it twice in 50+ years of playing.
I won once a few years after playing, and never again in the last 20 years.

This code attempts a few different things:
- provide some basic card and deck functionality
- provide a simulator framework to play the game
- (eventually) provide an AI framework to solve the game




## Original Performance Metrics
* typical size of move tree node at creation in old version was ~32K
* old values typically ranged from:
* depth 1
  * 1 MB for tree size
  * 10 MB for totally memory usage
- depth 2
  - 20-45 MB for tree size
  - 40-85 MB for totally memory usage
- depth 3
  - 700 MB-1GB for tree size
  - 1.3-2.0 GB for totally memory usage
- depth 4
  - consumed 14+GB ram

 ### byte arrays

 - list of byte arrays takes up 825-2800 bytes for 11 to 42 piles
 - 216 bytes for 1 pile, 3496 bytes for 52 piles