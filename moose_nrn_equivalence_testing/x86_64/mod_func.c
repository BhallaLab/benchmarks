#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _KChannel_HH_reg(void);
extern void _LeakConductance_reg(void);
extern void _NaChannel_HH_reg(void);
extern void _hd_reg(void);
extern void _kad_reg(void);
extern void _kap_reg(void);
extern void _kdr_reg(void);
extern void _na3_reg(void);
extern void _nax_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," chans/KChannel_HH.mod");
    fprintf(stderr," chans/LeakConductance.mod");
    fprintf(stderr," chans/NaChannel_HH.mod");
    fprintf(stderr," chans/hd.mod");
    fprintf(stderr," chans/kad.mod");
    fprintf(stderr," chans/kap.mod");
    fprintf(stderr," chans/kdr.mod");
    fprintf(stderr," chans/na3.mod");
    fprintf(stderr," chans/nax.mod");
    fprintf(stderr, "\n");
  }
  _KChannel_HH_reg();
  _LeakConductance_reg();
  _NaChannel_HH_reg();
  _hd_reg();
  _kad_reg();
  _kap_reg();
  _kdr_reg();
  _na3_reg();
  _nax_reg();
}
