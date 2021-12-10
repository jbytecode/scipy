# distutils: language=c++
# cython: language_level=3

from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "HConst.h" nogil:

    const int HIGHS_CONST_I_INF "kHighsIInf"
    const double HIGHS_CONST_INF "kHighsInf"
    const double kHighsTiny
    const double kHighsZero
    const int kHighsThreadLimit

    cdef enum HighsDebugLevel:
      HighsDebugLevel_kHighsDebugLevelNone "kHighsDebugLevelNone" = 0
      HighsDebugLevel_kHighsDebugLevelCheap "kHighsDebugLevelCheap"
      HighsDebugLevel_kHighsDebugLevelCostly "kHighsDebugLevelCostly"
      HighsDebugLevel_kHighsDebugLevelExpensive "kHighsDebugLevelExpensive"
      HighsDebugLevel_kHighsDebugLevelMin "kHighsDebugLevelMin" = HighsDebugLevel_kHighsDebugLevelNone
      HighsDebugLevel_kHighsDebugLevelMax "kHighsDebugLevelMax" = HighsDebugLevel_kHighsDebugLevelExpensive

    ctypedef enum HighsModelStatus:
        HighsModelStatusNOTSET "HighsModelStatus::kNotset" = 0
        HighsModelStatusLOAD_ERROR "HighsModelStatus::kLoadError"
        HighsModelStatusMODEL_ERROR "HighsModelStatus::kModelError"
        HighsModelStatusPRESOLVE_ERROR "HighsModelStatus::kPresolveError"
        HighsModelStatusSOLVE_ERROR "HighsModelStatus::kSolveError"
        HighsModelStatusPOSTSOLVE_ERROR "HighsModelStatus::kPostsolveError"
        HighsModelStatusMODEL_EMPTY "HighsModelStatus::kModelEmpty"
        HighsModelStatusOPTIMAL "HighsModelStatus::kOptimal"
        HighsModelStatusINFEASIBLE "HighsModelStatus::kInfeasible"
        HighsModelStatus_UNBOUNDED_OR_INFEASIBLE "HighsModelStatus::kUnboundedOrInfeasible"
        HighsModelStatusUNBOUNDED "HighsModelStatus::kUnbounded"
        HighsModelStatusREACHED_DUAL_OBJECTIVE_VALUE_UPPER_BOUND "HighsModelStatus::kObjectiveBound"
        HighsModelStatusREACHED_OBJECTIVE_TARGET "HighsModelStatus::kObjectiveTarget"
        HighsModelStatusREACHED_TIME_LIMIT "HighsModelStatus::kTimeLimit"
        HighsModelStatusREACHED_ITERATION_LIMIT "HighsModelStatus::kIterationLimit"
        HighsModelStatusUNKNOWN "HighsModelStatus::kUnknown"
        HighsModelStatusHIGHS_MODEL_STATUS_MIN "HighsModelStatus::kMin" = HighsModelStatusNOTSET
        HighsModelStatusHIGHS_MODEL_STATUS_MAX "HighsModelStatus::kMax" = HighsModelStatusUNKNOWN

    cdef enum HighsBasisStatus:
        HighsBasisStatusLOWER "HighsBasisStatus::kLower" = 0, # (slack) variable is at its lower bound [including fixed variables]
        HighsBasisStatusBASIC "HighsBasisStatus::kBasic" # (slack) variable is basic
        HighsBasisStatusUPPER "HighsBasisStatus::kUpper" # (slack) variable is at its upper bound
        HighsBasisStatusZERO "HighsBasisStatus::kZero" # free variable is non-basic and set to zero
        HighsBasisStatusNONBASIC "HighsBasisStatus::kNonbasic" # nonbasic with no specific bound information - useful for users and postsolve

    cdef enum SolverOption:
        SOLVER_OPTION_SIMPLEX "SolverOption::SOLVER_OPTION_SIMPLEX" = -1
        SOLVER_OPTION_CHOOSE "SolverOption::SOLVER_OPTION_CHOOSE"
        SOLVER_OPTION_IPM "SolverOption::SOLVER_OPTION_IPM"

    cdef enum PrimalDualStatus:
        PrimalDualStatusSTATUS_NOT_SET "PrimalDualStatus::STATUS_NOT_SET" = -1
        PrimalDualStatusSTATUS_MIN "PrimalDualStatus::STATUS_MIN" = PrimalDualStatusSTATUS_NOT_SET
        PrimalDualStatusSTATUS_NO_SOLUTION "PrimalDualStatus::STATUS_NO_SOLUTION"
        PrimalDualStatusSTATUS_UNKNOWN "PrimalDualStatus::STATUS_UNKNOWN"
        PrimalDualStatusSTATUS_INFEASIBLE_POINT "PrimalDualStatus::STATUS_INFEASIBLE_POINT"
        PrimalDualStatusSTATUS_FEASIBLE_POINT "PrimalDualStatus::STATUS_FEASIBLE_POINT"
        PrimalDualStatusSTATUS_MAX "PrimalDualStatus::STATUS_MAX" = PrimalDualStatusSTATUS_FEASIBLE_POINT

    cdef enum HighsOptionType:
        HighsOptionTypeBOOL "HighsOptionType::kBool" = 0
        HighsOptionTypeINT "HighsOptionType::kInt"
        HighsOptionTypeDOUBLE "HighsOptionType::kDouble"
        HighsOptionTypeSTRING "HighsOptionType::kString"

    ctypedef enum ObjSense:
        ObjSenseMINIMIZE "ObjSense::kMinimize" = 1
        ObjSenseMAXIMIZE "ObjSense::kMaximize" = -1

    cdef enum MatrixFormat:
        MatrixFormatkColwise "MatrixFormat::kColwise" = 1
        MatrixFormatkRowwise "MatrixFormat::kRowwise"
        MatrixFormatkRowwisePartitioned "MatrixFormat::kRowwisePartitioned"
