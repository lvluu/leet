"""Command-line interface for the animator."""

import argparse
from pathlib import Path
from typing import Optional

from .config import AnimationConfig
from .scenarios.registry import ScenarioRegistry


def main():
    parser = argparse.ArgumentParser(
        description="Generate DSA algorithm animations for GitBook"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate an animation")
    gen_parser.add_argument("scenario", help="Scenario name (e.g., sliding_window_fixed)")
    gen_parser.add_argument("-o", "--output", help="Output file path")
    gen_parser.add_argument("--speed", type=int, default=500, help="Frame duration in ms")
    gen_parser.add_argument("--data", help="Custom data as JSON array")

    # List command
    list_parser = subparsers.add_parser("list", help="List available scenarios")
    list_parser.add_argument("--pattern", help="Filter by pattern name")

    # Generate all command
    all_parser = subparsers.add_parser("generate-all", help="Generate all animations")
    all_parser.add_argument(
        "--output-dir",
        default="docs/.gitbook/assets/animations",
        help="Output directory",
    )
    all_parser.add_argument("--speed", type=int, default=500, help="Frame duration in ms")

    args = parser.parse_args()

    if args.command == "generate":
        return generate_animation(args)
    elif args.command == "list":
        return list_scenarios(args)
    elif args.command == "generate-all":
        return generate_all(args)
    else:
        parser.print_help()
        return 0


def generate_animation(args) -> int:
    """Generate a single animation from a scenario."""
    scenario = ScenarioRegistry.get(args.scenario)

    if not scenario:
        print(f"Error: Unknown scenario '{args.scenario}'")
        print("Run 'animator list' to see available scenarios")
        return 1

    config = AnimationConfig(frame_duration_ms=args.speed)

    animation = scenario.factory(config, data=args.data)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(config.output_dir) / scenario.pattern / f"{scenario.name}.gif"

    animation.export_gif(output_path)
    print(f"Generated: {output_path}")
    return 0


def list_scenarios(args) -> int:
    """List available scenarios."""
    print("Available scenarios:")
    print("-" * 60)

    for name, scenario in ScenarioRegistry.all():
        if args.pattern and args.pattern not in scenario.pattern:
            continue
        print(f"  {name:30} [{scenario.pattern}]")
        if scenario.description:
            print(f"    {scenario.description}")

    return 0


def generate_all(args) -> int:
    """Generate all animations."""
    config = AnimationConfig(
        frame_duration_ms=args.speed,
        output_dir=args.output_dir,
    )

    count = 0
    for name, scenario in ScenarioRegistry.all():
        output_path = Path(args.output_dir) / scenario.pattern / f"{name}.gif"
        animation = scenario.factory(config, data=None)
        animation.export_gif(output_path)
        print(f"Generated: {output_path}")
        count += 1

    print(f"\nGenerated {count} animations")
    return 0


if __name__ == "__main__":
    exit(main())
