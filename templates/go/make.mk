
manifest_files += go.mod
manifest_go.mod := go

goarch_aarch64 := GOARCH=arm64
goarch_armv7   := GOARCH=arm GOARM=7
go_flags_debug   := -gcflags='all=-N -l'
go_flags_release := -trimpath -ldflags='-s -w'
# Devshell CC'yi host derleyicisine ayarlar; CC tanımlıyken Go cross derlemede
# cgo'yu açar ve host derleyicisi hedefi derleyemez. Cross hedefte Go cgo'suz
# derlenir; cgo isteyen bir bileşen hedefin CC'si için ayrı bir karar ister.
go_env   = $(if $(CROSS),GOOS=linux $(goarch_$(TARGET)) CGO_ENABLED=0)
# `go build -o <dizin>` main paketi olmayan modülde hata verir: önce her paket
# derlenir, bin/'e yalnız main paketleri yazılır.
go_build = cd components/$1 && go generate ./... && $(go_env) go build $(go_flags_$(VARIANT)) ./... \
           && mains=$$($(go_env) go list -f '{{if eq .Name "main"}}{{.ImportPath}}{{end}}' ./...) \
           && { [ -z "$$mains" ] || $(go_env) go build $(go_flags_$(VARIANT)) -o $(BIN)/ $$mains; }
go_test  = cd components/$1 && go test -race ./...
go_lint  = cd components/$1 && golangci-lint run ./...
