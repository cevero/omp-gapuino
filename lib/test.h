#ifndef TEST_H
#define TEST_H

/* Needed for printf */
#include "gap_common.h"
#include "rtx_lib.h"

/* Needed for GAP8 Cluster usage */
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <stdlib.h>

#define FC_FREQ       (150000000)
#define CORE_NUMBER   (1)
#define SEED          (10)
#define V_MAX         (1200)
#define V_MIN         (1000)
#define V_STEP        (50)
#define F_MAX         (350000000)
#define F_MIN         (250000000)
#define F_STEP        (5000000)
#define F_DIV         (1000)
#define RUNS          (100000)
#define NUM_TESTS     (100)

#define TIMER TIMER1

struct run_info {
    int success_counter;
    int failure_counter;
    int call_total;
    int total_time;
};

#endif /* TEST_H */
