
manifest_files += buf.yaml
manifest_buf.yaml := proto

# Sözleşme bileşeni derlenmez: kodunu onu kullanan bileşen kendi build'inde
# üretir (Go `go generate`, Rust `build.rs`). Burada yalnız denetlenir.
proto_build = @:
proto_test  = @:
proto_lint  = cd components/$1 && buf lint
