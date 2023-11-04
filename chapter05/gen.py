import ninja
import pathlib
import sys


def cmd(*args):
    return " ".join(str(arg) for arg in args)


build_dir = pathlib.Path("build")
src_dir = pathlib.Path("src").joinpath("main").joinpath("java")
srcs = (path for path in src_dir.rglob("*.java"))

writer = ninja.Writer(sys.stdout)
writer.variable("src_dir", src_dir)
writer.variable("build_dir", build_dir)
writer.variable("flags", cmd("--class-path", "$src_dir", "-d", "$build_dir"))
writer.rule("regen_ninja", cmd(sys.executable, "$in", ">", "$out"))
writer.build("build.ninja", "regen_ninja", __file__)
writer.rule("javac", cmd("javac", "$flags", "$in"))
for src in srcs:
    rel_src = src.relative_to(src_dir)
    javafile = pathlib.Path("$src_dir").joinpath(rel_src)
    dst = pathlib.Path("$build_dir").joinpath(rel_src.with_suffix(".class"))
    writer.build(str(dst), "javac", str(javafile))
