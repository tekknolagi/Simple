import ninja
import pathlib

srcs = (path for path in pathlib.Path("src/main").rglob("*.java"))

with open("build.ninja", "w+") as f:
    writer = ninja.Writer(f)
    writer.rule(
        "javac",
        " ".join(
            ("javac", "-cp", "src/main/java", "--module-path", "src/main/java", "$in")
        ),
    )
    for src in srcs:
        dst = str(src).removesuffix(".java") + ".class"
        writer.build(dst, "javac", str(src))
