from __future__ import print_function
import os, subprocess

train_ids_dir = 'train_ids_dir'
outf = 'training_ids.txt'
outf_c = 'training_ids.zip'

if os.path.exists(outf_c):
    print("Are you sure you want to run this script? The ids are already scraped.")
    print("If so, please delete {} and re-run this.".format(outf))
    quit()

if not os.path.exists("train-labels-histogram.csv"):
    subprocess.call("wget https://research.google.com/youtube8m/csv/train-labels-histogram.csv",
                    shell = True)

if not os.path.exists(train_ids_dir):
    os.makedirs(train_ids_dir)

base = 'http://storage.googleapis.com/www.yt8m.org/csv/j/{}.js'

def get_ids_from_csv(csv_in, out_dir):
    with open(csv_in) as f:
        lines = f.readlines()[1:]
        for i, line in enumerate(lines):
            if i % 100 == 0: print("{}/{}".format(i, len(lines)))
            cid = line.split(",")[1].split("/")[-1]
            if os.path.exists('{}/{}'.format(out_dir, cid)): continue
            subprocess.call('wget --quiet {} -O {}/{}'.format(base.format(cid),
                                                              out_dir,
                                                              cid), shell = True)
            
get_ids_from_csv('train-labels-histogram.csv', train_ids_dir)

fs = [f for f in os.listdir(train_ids_dir) if f != 'README.md']
all_ids = []

for f in fs:
    with open('{}/{}'.format(train_ids_dir,f)) as g:
        cstr = g.read().strip()
        if len(cstr) == 0: continue
        cstr = cstr[:-1]
        x = cstr.split("\"")[-2]
        ids = x.split(';')
        all_ids.extend(ids)
        
with open(outf, 'w') as f:
    f.write('\n'.join(all_ids) + '\n')

print(outf, outf_c)
print('zip {} {}'.format(outf, outf_c))
subprocess.call('zip {} {}'.format(outf_c, outf), shell = True)
