PY=python3
DATE=$(shell date +%Y%m%d)

lock:
\tpip-compile --generate-hashes --output-file=requirements-hashes.txt requirements.txt

package:
\trm -rf libs
\tmkdir -p libs coldpkg
\tpip download --require-hashes -r requirements-hashes.txt -d libs
\tsha256sum libs/* > libs_checksums.txt
\tsha256sum scripts/* > scripts_checksums.txt
\trsync -a scripts/ coldpkg/scripts/
\tmkdir -p coldpkg/docs coldpkg/libs
\trsync -a libs/ coldpkg/libs/
\tcp libs_checksums.txt scripts_checksums.txt coldpkg/
\ttar -czf coldpkg-$(DATE).tar.gz coldpkg
