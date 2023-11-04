import ninja
import pathlib
import sys


def cmd(*args):
    return " ".join(str(arg) for arg in args)


build_dir = pathlib.Path("build")
src_dir = pathlib.Path("src/main/java")
srcs = (path for path in src_dir.rglob("*.java"))

writer = ninja.Writer(sys.stdout)
writer.variable("src_dir", src_dir)
writer.variable("build_dir", build_dir)
writer.variable("flags", cmd("--class-path", "$src_dir", "-d", "$build_dir"))
writer.rule("regen_ninja", cmd(sys.executable, "$in", ">", "$out"))
writer.build("build.ninja", "regen_ninja", __file__)
writer.rule("javac", cmd("javac", "$flags", "$in"))
for src in srcs:
    classfile = src.relative_to(src_dir).with_suffix(".class")
    dst = build_dir.joinpath(classfile)
    writer.build(str(dst), "javac", str(src))
