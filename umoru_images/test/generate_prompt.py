path = "data/test0717.txt"

prompt = "丸くて白いロボットが "
with open(path) as f:
        lines = f.readlines()
        for l in lines:
                prompt += l.rstrip('\n') + ", "

prompt += "をしてみたい様子"
print(prompt)
