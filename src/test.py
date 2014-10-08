canales = [473142857, # channel 14
479142857, # channel 15
485142857, # channel 16
491142857, # channel 17
497142857, # channel 18
503142857, # channel 19
509142857, # channel 20
515142857, # channel 21
521142857, # channel 22
527142857, # channel 23
533142857, # channel 24
539142857, # channel 25
545142857, # channel 26
551142857, # channel 27
557142857, # channel 28
563142857, # channel 29
569142857, # channel 30
575142857, # channel 31
581142857, # channel 32
587142857, # channel 33
593142857, # channel 34
599142857, # channel 35
605142857, # channel 36
617142857, # channel 38
623142857, # channel 39
629142857, # channel 40
635142857, # channel 41
641142857, # channel 42
647142857, # channel 43
653142857, # channel 44
659142857, # channel 45
665142857, # channel 46
671142857, # channel 47
677142857, # channel 48
683142857, # channel 49
689142857, # channel 50
695142857, # channel 51
701142857, # channel 52
707142857, # channel 53
713142857, # channel 54
719142857, # channel 55
725142857, # channel 56
731142857, # channel 57
737142857, # channel 58
743142857, # channel 59
749142857, # channel 60
755142857, # channel 61
761142857, # channel 62
767142857, # channel 63
773142857, # channel 64
779142857, # channel 65
785142857, # channel 66
791142857, # channel 67
797142857, # channel 68
803142857] # channel 69

import re

nro_canal = ' ([\d]+):'

porcentaje = 100.0/len(canales)

from subprocess import Popen, PIPE

cmd = ['scan', '/etc/huayra-tda-player/isdb-t.txt', '-q']
#cmd = ' '.join(cmd)

proc = Popen(cmd, stderr=PIPE, stdout=PIPE)

rep = 0

for line in iter(proc.stderr.readline, ''):
	if line.startswith('>>>'):
		canal_nro = int(re.findall(nro_canal, line)[0])
		if canal_nro in canales:
			rep += 1
			del(canales[canales.index(canal_nro)])

			print '%s%%' % (int(round(rep * porcentaje)), )

(data, err) = proc.communicate()
open('/tmp/test', 'w').write(data)
