from app.enums.mongo_operator_enum import MongoOperatorsEnum


class MongoPipelineBuilder:
    @staticmethod
    def replace_root_operator(new_root) -> dict:
        stage = {MongoOperatorsEnum.REPLACE_ROOT.value: {"newRoot": new_root}}
        return stage

    @staticmethod
    def match_operator(search_by) -> dict:
        stage = {MongoOperatorsEnum.MATCH.value: search_by}
        return stage

    @staticmethod
    def project_operator(project_by) -> dict:
        stage = {MongoOperatorsEnum.PROJECT.value: project_by}
        return stage

    @staticmethod
    def add_fields_operator(project_by) -> dict:
        stage = {MongoOperatorsEnum.ADDFIELDS.value: project_by}
        return stage

    @staticmethod
    def lookup_operator(from_coll, local_field, foreign_field,
                        data_as) -> dict:
        stage = {
            MongoOperatorsEnum.LOOKUP.value: {
                "from": from_coll,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": data_as
            }
        }
        return stage

    @staticmethod
    def unwind_operator(path, preserve_null_array=False) -> dict:
        stage = {MongoOperatorsEnum.UNWIND.value: {
            "path": path,
            "preserveNullAndEmptyArrays": preserve_null_array
        }}
        return stage

    @staticmethod
    def filter_operator(input, cond) -> dict:
        stage = {MongoOperatorsEnum.FILTER.value: {
            "input": input,
            "cond": cond
        }}
        return stage

    @staticmethod
    def group_operator(group_by) -> dict:
        stage = {MongoOperatorsEnum.GROUP.value: group_by}
        return stage

    @staticmethod
    def sort_operator(sort_by) -> dict:
        stage = {MongoOperatorsEnum.SORT.value: sort_by}
        return stage

    @staticmethod
    def skip_operator(skip_int) -> dict:
        stage = {MongoOperatorsEnum.SKIP.value: skip_int}
        return stage

    @staticmethod
    def limit_operator(limit_int) -> dict:
        stage = {MongoOperatorsEnum.LIMIT.value: limit_int}
        return stage

    @staticmethod
    def match_regex_operator(search_by, option) -> dict:
        stage = {
            MongoOperatorsEnum.REGEX.value: search_by,
            MongoOperatorsEnum.REGEX_OPTIONS.value: option
        }
        return stage

    @staticmethod
    def facet_operator(sub_pipelines) -> dict:
        stage = {MongoOperatorsEnum.FACET.value: sub_pipelines}
        return stage

    @staticmethod
    def lookup_with_let_operator(from_coll: str,
                                 let_var_dict: dict,
                                 pipeline: list, data_as: str) -> dict:
        stage = {
            MongoOperatorsEnum.LOOKUP.value: {
                "from": from_coll,
                "let": let_var_dict,
                "pipeline": pipeline,
                "as": data_as
            }
        }
        return stage

    @staticmethod
    def count_operator(key_name: str) -> dict:
        return {MongoOperatorsEnum.COUNT.value: key_name}
