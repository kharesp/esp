def create_repr(num_video_cams,output_dir):
  with open('%s/g%d.txt'%(output_dir,num_video_cams),'w') as outf:
    outf.write('vid;vtype;upstream\n')
    outf.write('v0;src;\n')
    tail_vertices=[] 
    for vnum in [13*x for x in range(num_video_cams)]:
      outf.write('v%d;bf;v0\n'%(vnum+1))
      outf.write('v%d;lpr;v%d\n'%(vnum+2,vnum+1))
      outf.write('v%d;eqh;v%d\n'%(vnum+3,vnum+1))
      outf.write('v%d;clahe;v%d\n'%(vnum+5,vnum+1))
      outf.write('v%d;lpr;v%d\n'%(vnum+4,vnum+3))
      outf.write('v%d;lpr;v%d\n'%(vnum+6,vnum+5))
      outf.write('v%d;eqh;v0\n'%(vnum+7))
      outf.write('v%d;lpr;v%d\n'%(vnum+8,vnum+7))
      outf.write('v%d;clahe;v0\n'%(vnum+9))
      outf.write('v%d;lpr;v%d\n'%(vnum+10,vnum+9))
      outf.write('v%d;seg;v%d,v%d\n'%(vnum+12,vnum+8,vnum+10))
      outf.write('v%d;seg;v%d,v%d,v%d\n'%(vnum+11,vnum+2,vnum+4,vnum+6))
      outf.write('v%d;fib;v%d\n'%(vnum+13,vnum+12))
      tail_vertices.extend(['v%d'%(vnum+11),'v%d'%(vnum+13)])
    outf.write('v%d;snk;%s\n'%(13*num_video_cams+1,','.join(tail_vertices)))

for vnum in range(3,7):
  create_repr(vnum,'dags/app')
