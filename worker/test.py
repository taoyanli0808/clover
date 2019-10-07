
from worker.worker import add


result = add.delay(4, 4)
print(result.get(1))
