from zipfile import ZipFile as ZF
import os

z = ZF('object_name.nvda-addon', 'w')
z.write('manifest.ini')
for l in os.listdir('globalPlugins'):
 z.write(os.path.join('globalPlugins', l))

z.close()
print 'Created addon.'
 