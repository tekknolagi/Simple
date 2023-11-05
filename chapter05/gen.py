import ninja
import pathlib
import sys


def cmd(*args):
    return " ".join(str(arg) for arg in args)


src_dir = pathlib.Path("src") / "main" / "java"

writer = ninja.Writer(sys.stdout)
writer.variable("src_dir", src_dir)
writer.variable("build_dir", "build")
writer.variable("flags", cmd("--class-path", "$src_dir", "-d", "$build_dir"))
writer.rule("regen_ninja", cmd(sys.executable, "$in", ">", "$out"))
writer.build("build.ninja", "regen_ninja", __file__)
writer.rule("javac", cmd("javac", "$flags", "$in"))
writer.rule(
    "jar",
    cmd(
        "jar",
        "--create",
        "--file",
        "$out",
        "--main-class",
        "com.seaofnodes.simple.Main",
        "-C",
        "$build_dir",
        ".",
    ),
)
classes = []
for src in src_dir.rglob("*.java"):
    rel_src = src.relative_to(src_dir)
    javafile = pathlib.Path("$src_dir") / rel_src
    dst = pathlib.Path("$build_dir") / rel_src.with_suffix(".class")
    classes += writer.build(str(dst), "javac", str(javafile))
writer.build("simple.jar", "jar", classes)
