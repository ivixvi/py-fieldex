from py_fieldex import Analyzer, CharFilter, Field, Filter, IndexTemplate, Tokenizer


def test_it():
    it = IndexTemplate(
        name="test",
        index_patterns=["test-*"],
        fields=[
            Field(name="all_updated_at", type_="long"),
            Field(
                name="company_name",
                type_="text",
                analyzer=Analyzer(
                    name="my_analyzer",
                    filters=[Filter("asciifolding")],
                    char_filters=[CharFilter(name="icu_normalizer")],
                    tokenizer=Tokenizer(name="keyword"),
                ),
                fields=[Field(name="long", type_="long")],
            ),
            Field(
                name="company_name_edge",
                type_="text",
                analyzer=Analyzer(
                    name="my_analyzer2",
                    filters=[
                        Filter(
                            "edge_ngram",
                            setting={
                                "type": "edge_ngram",
                                "min_gram": 1,
                                "max_gram": 2,
                            },
                        )
                    ],
                    char_filters=[
                        CharFilter(
                            name="mapping_replace",
                            setting={
                                "type": "mapping",
                                "mappings": [
                                    "٠ => 0",
                                    "١ => 1",
                                    "٢ => 2",
                                    "٣ => 3",
                                    "٤ => 4",
                                    "٥ => 5",
                                    "٦ => 6",
                                    "٧ => 7",
                                    "٨ => 8",
                                    "٩ => 9",
                                ],
                            },
                        )
                    ],
                    tokenizer=Tokenizer(
                        name="3digit",
                        setting={
                            "type": "simple_pattern",
                            "pattern": "[0123456789]{3}",
                        },
                    ),
                ),
            ),
        ],
    )
    expect_dict = {
        "index_patterns": ["test-*"],
        "settings": {
            "analysis": {
                "analyzers": {
                    "my_analyzer": {
                        "type": "custom",
                        "tokenizer": "keyword",
                        "filters": ["asciifolding"],
                        "char_filters": ["icu_normalizer"],
                    },
                    "my_analyzer2": {
                        "type": "custom",
                        "tokenizer": "3digit",
                        "filters": ["edge_ngram"],
                        "char_filters": ["mapping_replace"],
                    },
                },
                "tokenizer": {
                    "3digit": {"type": "simple_pattern", "pattern": "[0123456789]{3}"}
                },
                "filters": {
                    "edge_ngram": {"type": "edge_ngram", "min_gram": 1, "max_gram": 2}
                },
                "char_filters": {
                    "mapping_replace": {
                        "type": "mapping",
                        "mappings": [
                            "\u0660 => 0",
                            "\u0661 => 1",
                            "\u0662 => 2",
                            "\u0663 => 3",
                            "\u0664 => 4",
                            "\u0665 => 5",
                            "\u0666 => 6",
                            "\u0667 => 7",
                            "\u0668 => 8",
                            "\u0669 => 9",
                        ],
                    }
                },
            }
        },
        "mappings": {
            "properties": {
                "all_updated_at": {"type": "long"},
                "company_name": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                    "fields": {"long": {"type": "long"}},
                },
                "company_name_edge": {"type": "text", "analyzer": "my_analyzer2"},
            }
        },
    }
    assert "PUT _index_template/test" == it.put_path()
    assert expect_dict == it.build_template()
