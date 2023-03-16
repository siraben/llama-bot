{ pkgs ? import <nixpkgs> {}}:
with pkgs;

mkShell {
  packages = [ (python3.withPackages (ps: with ps; [ discordpy ])) ];
}
