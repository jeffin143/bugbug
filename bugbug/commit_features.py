# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import sys
from collections import defaultdict

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

EXPERIENCE_TIMESPAN = 90
EXPERIENCE_TIMESPAN_TEXT = f"{EXPERIENCE_TIMESPAN}_days"


class source_code_files_modified_num(object):
    name = "# of modified code files"

    def __call__(self, commit, **kwargs):
        return commit["source_code_files_modified_num"]


class other_files_modified_num(object):
    name = "# of modified non-code files"

    def __call__(self, commit, **kwargs):
        return commit["other_files_modified_num"]


class test_files_modified_num(object):
    name = "# of modified test files"

    def __call__(self, commit, **kwargs):
        return commit["test_files_modified_num"]


class source_code_file_size(object):
    def __call__(self, commit, **kwargs):
        return {
            "Total code files size": commit["total_source_code_file_size"],
            "Average code files size": commit["average_source_code_file_size"],
            "Maximum code files size": commit["maximum_source_code_file_size"],
            "Minimum code files size": commit["minimum_source_code_file_size"],
        }


class other_file_size(object):
    def __call__(self, commit, **kwargs):
        return {
            "Total non-code files size": commit["total_other_file_size"],
            "Average non-code files size": commit["average_other_file_size"],
            "Maximum non-code files size": commit["maximum_other_file_size"],
            "Minimum non-code files size": commit["minimum_other_file_size"],
        }


class test_file_size(object):
    def __call__(self, commit, **kwargs):
        return {
            "Total test files size": commit["total_test_file_size"],
            "Average test files size": commit["average_test_file_size"],
            "Maximum test files size": commit["maximum_test_file_size"],
            "Minimum test files size": commit["minimum_test_file_size"],
        }


class source_code_added(object):
    name = "# of code lines added"

    def __call__(self, commit, **kwargs):
        return commit["source_code_added"]


class other_added(object):
    name = "# of non-code lines added"

    def __call__(self, commit, **kwargs):
        return commit["other_added"]


class test_added(object):
    name = "# of lines added in tests"

    def __call__(self, commit, **kwargs):
        return commit["test_added"]


class source_code_deleted(object):
    name = "# of code lines deleted"

    def __call__(self, commit, **kwargs):
        return commit["source_code_deleted"]


class other_deleted(object):
    name = "# of non-code lines deleted"

    def __call__(self, commit, **kwargs):
        return commit["other_deleted"]


class test_deleted(object):
    name = "# of lines deleted in tests"

    def __call__(self, commit, **kwargs):
        return commit["test_deleted"]


def get_exps(exp_type, commit):
    items_key = f"{exp_type}s" if exp_type != "directory" else "directories"
    items_num = len(commit[items_key])

    return {
        "sum": commit[f"touched_prev_total_{exp_type}_sum"],
        "max": commit[f"touched_prev_total_{exp_type}_max"],
        "min": commit[f"touched_prev_total_{exp_type}_min"],
        "avg": commit[f"touched_prev_total_{exp_type}_sum"] / items_num
        if items_num > 0
        else 0,
        "sum backout": commit[f"touched_prev_total_{exp_type}_backout_sum"],
        "max backout": commit[f"touched_prev_total_{exp_type}_backout_max"],
        "min backout": commit[f"touched_prev_total_{exp_type}_backout_min"],
        "avg backout": commit[f"touched_prev_total_{exp_type}_backout_sum"] / items_num
        if items_num > 0
        else 0,
        f"sum {EXPERIENCE_TIMESPAN_TEXT}": commit[
            f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_{exp_type}_sum"
        ],
        f"max {EXPERIENCE_TIMESPAN_TEXT}": commit[
            f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_{exp_type}_max"
        ],
        f"min {EXPERIENCE_TIMESPAN_TEXT}": commit[
            f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_{exp_type}_min"
        ],
        f"avg {EXPERIENCE_TIMESPAN_TEXT}": commit[
            f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_{exp_type}_sum"
        ]
        / items_num
        if items_num > 0
        else 0,
        f"sum {EXPERIENCE_TIMESPAN_TEXT} backout": commit[
            f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_{exp_type}_backout_sum"
        ],
        f"max {EXPERIENCE_TIMESPAN_TEXT} backout": commit[
            f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_{exp_type}_backout_max"
        ],
        f"min {EXPERIENCE_TIMESPAN_TEXT} backout": commit[
            f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_{exp_type}_backout_min"
        ],
        f"avg {EXPERIENCE_TIMESPAN_TEXT} backout": commit[
            f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_{exp_type}_backout_sum"
        ]
        / items_num
        if items_num > 0
        else 0,
    }


class author_experience(object):
    name = "Author experience"

    def __call__(self, commit, **kwargs):
        return {
            "Author experience": commit["touched_prev_total_author_sum"],
            "Recent author experience": commit[
                f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_author_sum"
            ],
            "Author backouts": commit["touched_prev_total_author_backout_sum"],
            "Recent author backouts": commit[
                f"touched_prev_{EXPERIENCE_TIMESPAN_TEXT}_author_backout_sum"
            ],
            "Author seniority": commit["seniority_author"] / 86400,
        }


class reviewer_experience(object):
    def __call__(self, commit, **kwargs):
        exps = get_exps("reviewer", commit)
        return {
            "Total reviewer experience": exps["sum"],
            "Maximum reviewer experience": exps["max"],
            "Minimum reviewer experience": exps["min"],
            "Average reviewer experience": exps["avg"],
            "Total reviewer backouts": exps["sum backout"],
            "Maximum reviewer backouts": exps["max backout"],
            "Minimum reviewer backouts": exps["min backout"],
            "Average reviewer backouts": exps["avg backout"],
            "Total recent reviewer experience": exps[f"sum {EXPERIENCE_TIMESPAN_TEXT}"],
            "Maximum recent reviewer experience": exps[
                f"max {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Minimum recent reviewer experience": exps[
                f"min {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Average recent reviewer experience": exps[
                f"avg {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Total recent reviewer backouts": exps[
                f"sum {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Maximum recent reviewer backouts": exps[
                f"max {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Minimum recent reviewer backouts": exps[
                f"min {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Average recent reviewer backouts": exps[
                f"avg {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
        }


class reviewers_num(object):
    name = "# of reviewers"

    def __call__(self, commit, **kwargs):
        return len(commit["reviewers"])


class components(object):
    def __call__(self, commit, **kwargs):
        return commit["components"]


class components_modified_num(object):
    name = "# of components modified"

    def __call__(self, commit, **kwargs):
        return len(commit["components"])


class component_touched_prev(object):
    def __call__(self, commit, **kwargs):
        exps = get_exps("component", commit)
        return {
            "Total # of times these components have been touched before": exps["sum"],
            "Maximum # of times these components have been touched before": exps["max"],
            "Minimum # of times these components have been touched before": exps["min"],
            "Average # of times these components have been touched before": exps["avg"],
            "Total # of backouts in these components": exps["sum backout"],
            "Maximum # of backouts in these components": exps["max backout"],
            "Minimum # of backouts in these components": exps["min backout"],
            "Average # of backouts in these components": exps["avg backout"],
            "Total # of times these components have recently been touched": exps[
                f"sum {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Maximum # of times these components have recently been touched": exps[
                f"max {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Minimum # of times these components have recently been touched": exps[
                f"min {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Average # of times these components have recently been touched": exps[
                f"avg {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Total # of recent backouts in these components": exps[
                f"sum {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Maximum # of recent backouts in these components": exps[
                f"max {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Minimum # of recent backouts in these components": exps[
                f"min {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Average # of recent backouts in these components": exps[
                f"avg {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
        }


class directories(object):
    def __call__(self, commit, **kwargs):
        return commit["directories"]


class directories_modified_num(object):
    name = "# of directories modified"

    def __call__(self, commit, **kwargs):
        return len(commit["directories"])


class directory_touched_prev(object):
    def __call__(self, commit, **kwargs):
        exps = get_exps("directory", commit)
        return {
            "Total # of times these directories have been touched before": exps["sum"],
            "Maximum # of times these directories have been touched before": exps[
                "max"
            ],
            "Minimum # of times these directories have been touched before": exps[
                "min"
            ],
            "Average # of times these directories have been touched before": exps[
                "avg"
            ],
            "Total # of backouts in these directories": exps["sum backout"],
            "Maximum # of backouts in these directories": exps["max backout"],
            "Minimum # of backouts in these directories": exps["min backout"],
            "Average # of backouts in these directories": exps["avg backout"],
            "Total # of times these directories have recently been touched": exps[
                f"sum {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Maximum # of times these directories have recently been touched": exps[
                f"max {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Minimum # of times these directories have recently been touched": exps[
                f"min {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Average # of times these directories have recently been touched": exps[
                f"avg {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Total # of recent backouts in these directories": exps[
                f"sum {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Maximum # of recent backouts in these directories": exps[
                f"max {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Minimum # of recent backouts in these directories": exps[
                f"min {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Average # of recent backouts in these directories": exps[
                f"avg {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
        }


class files(object):
    def __init__(self, min_freq=0.0014):
        self.min_freq = min_freq

    def fit(self, commits):
        self.count = defaultdict(int)

        self.total_commits = 0

        for commit in commits:
            self.total_commits += 1

            for f in commit["files"]:
                self.count[f] += 1

        # We no longer need to store counts for files which have low frequency.
        to_del = set()
        for f, c in self.count.items():
            if c / self.total_commits < self.min_freq:
                to_del.add(f)

        for f in to_del:
            del self.count[f]

    def __call__(self, commit, **kwargs):
        return [
            f
            for f in commit["files"]
            if (self.count[f] / self.total_commits) > self.min_freq
        ]


class file_touched_prev(object):
    def __call__(self, commit, **kwargs):
        exps = get_exps("component", commit)
        return {
            "Total # of times these files have been touched before": exps["sum"],
            "Maximum # of times these files have been touched before": exps["max"],
            "Minimum # of times these files have been touched before": exps["min"],
            "Average # of times these files have been touched before": exps["avg"],
            "Total # of backouts in these files": exps["sum backout"],
            "Maximum # of backouts in these files": exps["max backout"],
            "Minimum # of backouts in these files": exps["min backout"],
            "Average # of backouts in these files": exps["avg backout"],
            "Total # of times these files have recently been touched": exps[
                f"sum {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Maximum # of times these files have recently been touched": exps[
                f"max {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Minimum # of times these files have recently been touched": exps[
                f"min {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Average # of times these files have recently been touched": exps[
                f"avg {EXPERIENCE_TIMESPAN_TEXT}"
            ],
            "Total # of recent backouts in these files": exps[
                f"sum {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Maximum # of recent backouts in these files": exps[
                f"max {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Minimum # of recent backouts in these files": exps[
                f"min {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
            "Average # of recent backouts in these files": exps[
                f"avg {EXPERIENCE_TIMESPAN_TEXT} backout"
            ],
        }


class types(object):
    name = "file types"

    def __call__(self, commit, **kwargs):
        return commit["types"]


def merge_commits(commits):
    return {
        "nodes": tuple(commit["node"] for commit in commits),
        "pushdate": commits[0]["pushdate"],
        "types": tuple(set(sum((commit["types"] for commit in commits), []))),
        "files": tuple(set(sum((commit["files"] for commit in commits), []))),
        "directories": tuple(
            set(sum((commit["directories"] for commit in commits), []))
        ),
        "components": tuple(set(sum((commit["components"] for commit in commits), []))),
    }


class CommitExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, feature_extractors, cleanup_functions):
        self.feature_extractors = feature_extractors
        self.cleanup_functions = cleanup_functions

    def fit(self, x, y=None):
        for feature in self.feature_extractors:
            if hasattr(feature, "fit"):
                feature.fit(x())

        return self

    def transform(self, commits):
        results = []

        for commit in commits():
            data = {}

            for feature_extractor in self.feature_extractors:
                if "bug_features" in feature_extractor.__module__:
                    if not commit["bug"]:
                        continue

                    res = feature_extractor(commit["bug"])
                elif "test_scheduling_features" in feature_extractor.__module__:
                    res = feature_extractor(commit["test_job"])
                else:
                    res = feature_extractor(commit)

                if res is None:
                    continue

                if hasattr(feature_extractor, "name"):
                    feature_extractor_name = feature_extractor.name
                else:
                    feature_extractor_name = feature_extractor.__class__.__name__

                if isinstance(res, dict):
                    for key, value in res.items():
                        data[sys.intern(key)] = value
                    continue

                if isinstance(res, list):
                    for item in res:
                        data[sys.intern(f"{item} in {feature_extractor_name}")] = "True"
                    continue

                if isinstance(res, bool):
                    res = str(res)

                data[sys.intern(feature_extractor_name)] = res

            # TODO: Try simply using all possible fields instead of extracting features manually.

            for cleanup_function in self.cleanup_functions:
                commit["desc"] = cleanup_function(commit["desc"])

            result = {"data": data, "desc": commit["desc"]}

            results.append(result)

        return pd.DataFrame(results)
