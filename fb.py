#encoding: utf-8
states = ('t', 'f')

obs =  '01010101000000000010101010'

start_prob = {'t': 0.5, 'f': 0.5}

transition_prob = {
   't' : {'t': 0.8, 'f': 0.2},
   'f' : {'t': 0.3, 'f': 0.7}
   }

emission_prob = {
   't' : {'0': 0.1, '1': 0.9},
   'f' : {'0': 0.9, '1': 0.1}
   }

#прямой проход

FWtrue = list([start_prob['t']*emission_prob['t'][obs[0]]])  
FWfalse = list([start_prob['f']*emission_prob['f'][obs[0]]]) 
                
for v in obs[1:]:
  FWtrue.append(sum([FWtrue[-1]*transition_prob['t']['t']*emission_prob['t'][v],
                    FWfalse[-1]*transition_prob['f']['t']*emission_prob['t'][v]]))
  
  FWfalse.append(sum([FWfalse[-1]*transition_prob['f']['f']*emission_prob['f'][v],
                     FWtrue[-2]*transition_prob['t']['f']*emission_prob['f'][v]]))
  
  
#обратный проход

BWtrue = list([emission_prob['t'][obs[-1]]])
BWfalse = list([emission_prob['f'][obs[-1]]])


for v in obs[:-1][::-1]:

  BWtrue.append(sum([BWtrue[-1]*transition_prob['t']['t']*emission_prob['t'][v],
                    BWfalse[-1]*transition_prob['t']['f']*emission_prob['t'][v]]))
  
  BWfalse.append(sum([BWtrue[-2]*transition_prob['f']['t']*emission_prob['f'][v],
                     BWfalse[-1]*transition_prob['f']['f']*emission_prob['f'][v]]))  
  
BWtrue = BWtrue[::-1]
BWfalse = BWfalse[::-1]
  
#нормализация
  
 
true_line = []
false_line = []

for x in range(len(obs)):
  true = FWtrue[x]*BWtrue[x]/emission_prob['t'][obs[x]]
  false = FWfalse[x]*BWfalse[x]/emission_prob['f'][obs[x]]
  both = true + false
  
  true_line.append(round(true/both, 2))
  false_line.append(round(false/both, 2))
  
  
print(true_line)
print(false_line)
  
