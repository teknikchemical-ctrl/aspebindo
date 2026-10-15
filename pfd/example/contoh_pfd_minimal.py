# -*- coding: utf-8 -*-
# Contoh pemakaian minimal mesin PFD (eng.py), dijalankan dari folder pfd_engine/
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eng

d = eng.Doc()
d.eq('vessel', 'V-101', 20, 30, 20, 40)
d.eq('pump',   'P-101', 60, 20, 8, 8)
d.conn('1', 'V-101.b', 'P-101.l', num=1)      # sambungan proses dengan nomor aliran
d.flag('UMPAN', 5, 50, d='r', kind='in')      # bendera batas masuk
d.text(10, 80, 'CONTOH PFD MINIMAL', 4, 'l', True)
d.finalize()                                   # WAJIB sebelum pdf(): hitung celah persilangan & panah
d.pdf(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contoh_pfd_minimal.pdf'))
print('selesai ->', 'contoh_pfd_minimal.pdf')
