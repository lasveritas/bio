states = ('t', 'f')
observations =  '001010101010000000000000000000000001010101010' 

start_probability = {'t': 0.5, 'f': 0.5}
 
transition_probability = {
   't' : {'t': 0.5, 'f': 0.5},
   'f' : {'t': 0.5, 'f': 0.5}
   }
 
emission_probability = {
   't' : {'0': 0.5, '1': 0.5},
   'f' : {'0': 0.9, '1': 0.1}
   }


def viterbi(obs, states, start_p, trans_p, emit_p):
  V = [{}]
  path = {}
    
  for y in states:
    V[0][y] = start_p[y] * emit_p[y][obs[0]]
    path[y] = [y]
    
  for t in range(1, len(obs)):
    V.append({})
    newpath = {}

    for y in states:
      (prob, state) =  max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
      V[t][y] = prob
      newpath[y] = path[state] + [y]
              
    path = newpath
    
  n = len(obs) - 1
  (prob, state) = max((V[n][y], y) for y in states)
  result = ''
  for i in path[state]:
    result += i
  return (prob, result)
  

print(observations +'\n' + viterbi (observations, states, start_probability, transition_probability, emission_probability)[1]) 