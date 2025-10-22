"""Orchestrator / CLI entry for resume_ai_pipeline.
This is a minimal stub to run basic commands.
"""

import argparse
from pathlib import Path

from . import ingest, retriever, ats_scoring


def main():
    parser = argparse.ArgumentParser(description="Resume AI Pipeline CLI")
    sub = parser.add_subparsers(dest="cmd")

    parser_ingest = sub.add_parser("ingest", help="Ingest a resume file")
    parser_ingest.add_argument("path", type=str, help="Path to resume file")

    parser_query = sub.add_parser("query", help="Query the vector store")
    parser_query.add_argument("q", type=str, help="Query string")

    parser_score = sub.add_parser("score", help="Score a resume file")
    parser_score.add_argument("path", type=str, help="Path to resume file")

    args = parser.parse_args()

    if args.cmd == "ingest":
        print(ingest.ingest_file(args.path))
    elif args.cmd == "query":
        r = retriever.Retriever()
        print(r.retrieve(args.q))
    elif args.cmd == "score":
        print(ats_scoring.score_resume_from_path(args.path))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
