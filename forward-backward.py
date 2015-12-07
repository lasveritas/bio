#encoding: utf-8
states = ('t', 'f')
end_state  = ('E')

observations =  ('0', '1', '0', '1', '1', '1')

start_probability = {'t': 0.5, 'f': 0.5}

transition_probability = {
   't' : {'t': 0.79, 'f': 0.2, 'E': 0.01},
   'f' : {'t': 0.3, 'f': 0.69, 'E': 0.01}
   }

emission_probability = {
   't' : {'0': 0.5, '1': 0.5},
   'f' : {'0': 0.9, '1': 0.1}
   }

def fwd_bkw(obs, states, start, tr, em, end_st):
    N = len(obs)
 
    fwd = []
    f_prev = {}
    
    # прямой проход
    for i, obs_i in enumerate(obs):
        f_curr = {}
        for st in states:
            if i == 0:
                #начальное заполнение
                prevFWsum = start[st]
            else:
                #вероятность попасть из прошлого состояние в нынешнее
                prevFWsum = sum(f_prev[k]*tr[k][st] for k in states)
 
            f_curr[st] = em[st][obs_i] * prevFWsum
 
        fwd.append(f_curr)
        f_prev = f_curr
 
    #уход в конец    
    p_fwd = sum(f_curr[k]*tr[k][end_st] for k in states)
 
    bkw = []
    b_prev = {}
    # обратный проход
    for i, obs_i_plus in enumerate((None,)+obs[::-1][:-1]):
     
        b_curr = {}
        for st in states:
            if i == 0:
                # base case for backward part
                b_curr[st] = tr[st][end_st]
            else:
                b_curr[st] = sum(tr[st][l]*em[l][obs_i_plus]*b_prev[l] for l in states)
 
        bkw.insert(0,b_curr)
        b_prev = b_curr
 
    p_bkw = sum(start[l] * em[l][obs[0]] * b_curr[l] for l in states)
 
    # merging the two parts
    posterior = []
    for i in range(N):
        posterior.append({st: fwd[i][st]*bkw[i][st]/p_fwd for st in states})
 
    assert p_fwd == p_bkw
    return fwd, bkw, posterior

  
def example():
    return fwd_bkw(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability,
                   end_state)

for line in example():
    print(' '.join(map(str, line)))  