{
    description = "dataset generator";

    inputs = {
        nixpkgs.url = "nixpkgs/nixos-unstable";
    };

    outputs = { self, nixpkgs }: let
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in {
        devShells.x86_64-linux.default = pkgs.mkShell {
            packages = with pkgs; [
                sqlite-interactive
                python311Packages.transformers
                python311Packages.pytorch
            ];
        };
    };
}
