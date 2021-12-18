# distutils: language=c++
# cython: language_level=3

'''Export enum values and constants from HiGHS.'''

from .HConst cimport (
    HIGHS_CONST_I_INF,
    HIGHS_CONST_INF,

    HighsDebugLevel_kHighsDebugLevelNone,
    HighsDebugLevel_kHighsDebugLevelCheap,

    HighsModelStatusNOTSET,
    HighsModelStatusLOAD_ERROR,
    HighsModelStatusMODEL_ERROR,
    HighsModelStatusMODEL_EMPTY,
    HighsModelStatusPRESOLVE_ERROR,
    HighsModelStatusSOLVE_ERROR,
    HighsModelStatusPOSTSOLVE_ERROR,
    HighsModelStatusINFEASIBLE,
    HighsModelStatusUNBOUNDED,
    HighsModelStatusOPTIMAL,
    HighsModelStatusREACHED_DUAL_OBJECTIVE_VALUE_UPPER_BOUND,
    HighsModelStatusREACHED_TIME_LIMIT,
    HighsModelStatusREACHED_ITERATION_LIMIT,

    ObjSenseMINIMIZE,
    kContinuous,
    kInteger,
    kSemiContinuous,
    kSemiInteger,
    kImplicitInteger,
)
from .HighsIO cimport (
    kInfo,
    kDetailed,
    kVerbose,
    kWarning,
    kError,
)
from .SimplexConst cimport (
    # Simplex strategy
    SIMPLEX_STRATEGY_CHOOSE,
    SIMPLEX_STRATEGY_DUAL,
    SIMPLEX_STRATEGY_PRIMAL,

    # Crash strategy
    SIMPLEX_CRASH_STRATEGY_OFF,
    SIMPLEX_CRASH_STRATEGY_BIXBY,
    SIMPLEX_CRASH_STRATEGY_LTSF,

    # Dual edge weight strategy
    SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_CHOOSE,
    SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_DANTZIG,
    SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_DEVEX,
    SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_STEEPEST_EDGE,
    SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_STEEPEST_EDGE_UNIT_INITIAL,

    # Primal edge weight strategy
    SIMPLEX_PRIMAL_EDGE_WEIGHT_STRATEGY_DANTZIG,
    SIMPLEX_PRIMAL_EDGE_WEIGHT_STRATEGY_CHOOSE,
    SIMPLEX_PRIMAL_EDGE_WEIGHT_STRATEGY_DEVEX,
)

# HConst
CONST_I_INF = HIGHS_CONST_I_INF
CONST_INF = HIGHS_CONST_INF

# Debug level
MESSAGE_LEVEL_NONE = HighsDebugLevel_kHighsDebugLevelNone
MESSAGE_LEVEL_MINIMAL = HighsDebugLevel_kHighsDebugLevelCheap

# HighsIO
LOG_TYPE_INFO = <int> kInfo
LOG_TYPE_DETAILED = <int> kDetailed
LOG_TYPE_VERBOSE = <int> kVerbose
LOG_TYPE_WARNING = <int> kWarning
LOG_TYPE_ERROR = <int> kError

# HighsLp
MODEL_STATUS_NOTSET = <int> HighsModelStatusNOTSET
MODEL_STATUS_LOAD_ERROR = <int> HighsModelStatusLOAD_ERROR
MODEL_STATUS_MODEL_ERROR = <int> HighsModelStatusMODEL_ERROR
MODEL_STATUS_PRESOLVE_ERROR = <int> HighsModelStatusPRESOLVE_ERROR
MODEL_STATUS_SOLVE_ERROR = <int> HighsModelStatusSOLVE_ERROR
MODEL_STATUS_POSTSOLVE_ERROR = <int> HighsModelStatusPOSTSOLVE_ERROR
MODEL_STATUS_MODEL_EMPTY = <int> HighsModelStatusMODEL_EMPTY
MODEL_STATUS_INFEASIBLE = <int> HighsModelStatusINFEASIBLE
MODEL_STATUS_UNBOUNDED = <int> HighsModelStatusUNBOUNDED
MODEL_STATUS_OPTIMAL = <int> HighsModelStatusOPTIMAL
MODEL_STATUS_REACHED_DUAL_OBJECTIVE_VALUE_UPPER_BOUND = <int> HighsModelStatusREACHED_DUAL_OBJECTIVE_VALUE_UPPER_BOUND
MODEL_STATUS_REACHED_TIME_LIMIT = <int> HighsModelStatusREACHED_TIME_LIMIT
MODEL_STATUS_REACHED_ITERATION_LIMIT = <int> HighsModelStatusREACHED_ITERATION_LIMIT

# Simplex strategy
HIGHS_SIMPLEX_STRATEGY_CHOOSE = <int> SIMPLEX_STRATEGY_CHOOSE
HIGHS_SIMPLEX_STRATEGY_DUAL = <int> SIMPLEX_STRATEGY_DUAL
HIGHS_SIMPLEX_STRATEGY_PRIMAL = <int> SIMPLEX_STRATEGY_PRIMAL

# Crash strategy
HIGHS_SIMPLEX_CRASH_STRATEGY_OFF = <int> SIMPLEX_CRASH_STRATEGY_OFF
HIGHS_SIMPLEX_CRASH_STRATEGY_BIXBY = <int> SIMPLEX_CRASH_STRATEGY_BIXBY
HIGHS_SIMPLEX_CRASH_STRATEGY_LTSF = <int> SIMPLEX_CRASH_STRATEGY_LTSF

# Dual edge weight strategy
HIGHS_SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_CHOOSE = <int> SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_CHOOSE
HIGHS_SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_DANTZIG = <int> SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_DANTZIG
HIGHS_SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_DEVEX = <int> SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_DEVEX
HIGHS_SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_STEEPEST_EDGE = <int> SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_STEEPEST_EDGE
# HIGHS_SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_STEEPEST_EDGE_UNIT_INITIAL = <int> SIMPLEX_DUAL_EDGE_WEIGHT_STRATEGY_STEEPEST_EDGE_UNIT_INITIAL

# Primal edge weight strategy
HIGHS_SIMPLEX_PRIMAL_EDGE_WEIGHT_STRATEGY_CHOOSE = <int> SIMPLEX_PRIMAL_EDGE_WEIGHT_STRATEGY_CHOOSE
HIGHS_SIMPLEX_PRIMAL_EDGE_WEIGHT_STRATEGY_DANTZIG = <int> SIMPLEX_PRIMAL_EDGE_WEIGHT_STRATEGY_DANTZIG
HIGHS_SIMPLEX_PRIMAL_EDGE_WEIGHT_STRATEGY_DEVEX = <int> SIMPLEX_PRIMAL_EDGE_WEIGHT_STRATEGY_DEVEX

# Objective sense
HIGHS_OBJECTIVE_SENSE_MINIMIZE = <int> ObjSenseMINIMIZE

# Variable types
HIGHS_VAR_TYPE_CONTINUOUS = <int> kContinuous
HIGHS_VAR_TYPE_INTEGER = <int> kInteger
HIGHS_VAR_TYPE_SEMI_CONTINUOUS = <int> kSemiContinuous
HIGHS_VAR_TYPE_SEMI_INTEGER = <int> kSemiInteger
HIGHS_VAR_TYPE_IMPLICIT_INTEGER = <int> kImplicitInteger
