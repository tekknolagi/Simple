package com.seaofnodes.simple;

import com.seaofnodes.simple.node.*;

class Main {
  public static void main(String[] args) {
    System.out.println("hi!");
    Parser p = new Parser("int a = 3;");
    StopNode result = p.parse();
    System.out.println(result);
  }
}
