from enum import StrEnum


class MongoUpdateOperatorsEnum(StrEnum):
    SET = "$set"
    PUSH = "$push"
    EACH = "$each"
    POSITION = "$position"
    PULL = "$pull"


class MongoOperatorsEnum(StrEnum):
    SLICE = "$slice"
    FILTER = "$filter"
    UNWIND = "$unwind"
    LOOKUP = "$lookup"
    ADDFIELDS = "$addFields"
    PROJECT = "$project"
    MATCH = "$match"
    GROUP = "$group"
    SORT = "$sort"
    SKIP = "$skip"
    LIMIT = "$limit"
    REGEX = "$regex"
    REGEX_OPTIONS = "$options"
    IFNULL = "$ifNull"
    FACET = "$facet"
    COUNT = "$count"
    REPLACE_ROOT = "$replaceRoot"
    COND = "$cond"
    TYPE = '$type'
    EXPR = "$expr"
    REDUCE = "$reduce"
    EXISTS = "$exists"
    TOLOWER = "$toLower"


class MongoGroupOperatorsEnum(StrEnum):
    FIRST = "$first"
    ADDTOSET = "$addToSet"
    PUSH = "$push"


class MongoLogicalOperatorsEnum(StrEnum):
    AND = "$and"
    OR = "$or"
    EQUAL = "$eq"
    IN = "$in"
    NOT_IN = "$nin"
    NOT_EQUAL = "$ne"
    GREATER_THAN = "$gt"
    GREATER_OR_EQUAL = "$gte"
    LESS_THAN = "$lt"
    LESS_THAN_OR_EQUAL = "$lte"


class MongoFilterOperatorsEnum(StrEnum):
    SIZE = "$size"


class MongoDataConversionOperatorsEnum(StrEnum):
    TO_STRING = "$toString"
    TO_LOWER = "$toLower"
    CONCAT = "$concat"
    SUBSTR = "$substr"
