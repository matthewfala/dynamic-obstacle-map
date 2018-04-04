import json

class SimWriter:

  def __init__(self, fileName):
    self.fileName = fileName
    self.data = {}
    self.data['ticks'] = []

  def append(self, tick, currentState):
    self.data['ticks'].append({
       'tick': tick,
       'position' : {'x' : currentState.position.x, 'y' : currentState.position.y, 'z' : currentState.position.z}
    })

  def writeFile(self):
    with open(self.fileName, 'w') as outfile:
      outfile.write(json.dumps(self.data, indent=4, sort_keys=True))
      outfile.close()




