#!/bin/bash
# Script para criar AppImage do Echo Cleaner
# Uso: ./build_appimage.sh

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Echo Cleaner - AppImage Builder      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"

# Variáveis
APP_NAME="EchoCleaner"
APP_DIR="build/${APP_NAME}.AppDir"
VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2 2>/dev/null || echo "0.2.0")
OUTPUT_NAME="${APP_NAME}-x86_64.AppImage"

# Verificar se appimagetool existe
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    echo -e "${RED}Error: appimagetool-x86_64.AppImage not found!${NC}"
    echo "Download it from: https://github.com/AppImage/AppImageKit/releases"
    exit 1
fi

# Garantir que appimagetool é executável
chmod +x appimagetool-x86_64.AppImage

# Criar/atualizar estrutura AppDir
echo -e "${YELLOW}Step 1: Creating/updating AppDir structure...${NC}"

# Criar diretórios necessários
mkdir -p "${APP_DIR}/usr/bin"
mkdir -p "${APP_DIR}/usr/share/applications"
mkdir -p "${APP_DIR}/usr/share/icons/hicolor/256x256/apps"
mkdir -p "${APP_DIR}/usr/lib/python3/dist-packages"

# Copiar aplicação
echo -e "${YELLOW}Step 2: Copying application files...${NC}"
cp -r app "${APP_DIR}/usr/lib/python3/dist-packages/"
cp echo-cleaner.py "${APP_DIR}/usr/lib/python3/dist-packages/"
cp requirements.txt "${APP_DIR}/usr/lib/python3/dist-packages/"

# Criar script executável principal
echo -e "${YELLOW}Step 3: Creating launcher script...${NC}"
cat > "${APP_DIR}/usr/bin/${APP_NAME}" << 'EOFBIN'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
APP_DIR="${HERE}/../"

# Adicionar Python ao PATH
export PYTHONPATH="${APP_DIR}/usr/lib/python3/dist-packages:${PYTHONPATH}"

# Usar o Python do sistema
exec python3 "${APP_DIR}/usr/lib/python3/dist-packages/echo-cleaner.py" "$@"
EOFBIN

chmod +x "${APP_DIR}/usr/bin/${APP_NAME}"

# Copiar/criar arquivo .desktop
echo -e "${YELLOW}Step 4: Setting up desktop entry...${NC}"
cat > "${APP_DIR}/${APP_NAME}.desktop" << 'EOFDESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=Echo Cleaner
Comment=Intelligent System Cleaner for Linux
Exec=EchoCleaner
Icon=EchoCleaner
Terminal=false
Categories=System;
Keywords=clean;cleaner;cache;disk;space;docker;
StartupNotify=true
EOFDESKTOP

# Copiar para usr/share/applications também
cp "${APP_DIR}/${APP_NAME}.desktop" "${APP_DIR}/usr/share/applications/"

# Criar ícone (PNG simples se não existir)
echo -e "${YELLOW}Step 5: Setting up icon...${NC}"
if [ -f "app/assets/icon.png" ]; then
    cp app/assets/icon.png "${APP_DIR}/${APP_NAME}.png"
    cp app/assets/icon.png "${APP_DIR}/usr/share/icons/hicolor/256x256/apps/${APP_NAME}.png"
else
    # Criar um ícone placeholder se não existir
    echo -e "${YELLOW}Warning: No icon found, creating placeholder...${NC}"
    # Usar ImageMagick se disponível
    if command -v convert &> /dev/null; then
        convert -size 256x256 xc:blue -pointsize 72 -fill white -gravity center \
                -annotate +0+0 "EC" "${APP_DIR}/${APP_NAME}.png"
        cp "${APP_DIR}/${APP_NAME}.png" "${APP_DIR}/usr/share/icons/hicolor/256x256/apps/"
    else
        echo -e "${RED}ImageMagick not found, skipping icon creation${NC}"
    fi
fi

# Copiar ícone como .DirIcon
if [ -f "${APP_DIR}/${APP_NAME}.png" ]; then
    cp "${APP_DIR}/${APP_NAME}.png" "${APP_DIR}/.DirIcon"
fi

# Criar AppRun
echo -e "${YELLOW}Step 6: Creating AppRun launcher...${NC}"
cat > "${APP_DIR}/AppRun" << 'EOFAPPRUN'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}

export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
export PYTHONPATH="${HERE}/usr/lib/python3/dist-packages:${PYTHONPATH}"

# Verificar se Python3 está disponível
if ! command -v python3 &> /dev/null; then
    zenity --error --text="Python 3 is required but not found!\nPlease install Python 3 to run Echo Cleaner." 2>/dev/null || \
    echo "Error: Python 3 is required but not found!" >&2
    exit 1
fi

# Verificar se PySide6 está instalível
if ! python3 -c "import PySide6" 2>/dev/null; then
    MESSAGE="PySide6 is required but not found!\n\nInstall it with:\nsudo apt install python3-pyside6.qtwidgets python3-pyside6.qtcore python3-pyside6.qtgui\n\nOr with pip:\npip3 install PySide6"
    zenity --error --text="$MESSAGE" 2>/dev/null || echo -e "$MESSAGE" >&2
    exit 1
fi

exec "${HERE}/usr/bin/EchoCleaner" "$@"
EOFAPPRUN

chmod +x "${APP_DIR}/AppRun"

# Criar AppImage
echo -e "${YELLOW}Step 7: Building AppImage...${NC}"

# Remover AppImage anterior se existir
if [ -f "${OUTPUT_NAME}" ]; then
    echo -e "${YELLOW}Removing old AppImage...${NC}"
    rm "${OUTPUT_NAME}"
fi

# Executar appimagetool
ARCH=x86_64 ./appimagetool-x86_64.AppImage "${APP_DIR}" "${OUTPUT_NAME}"

if [ -f "${OUTPUT_NAME}" ]; then
    chmod +x "${OUTPUT_NAME}"
    echo -e "\n${GREEN}Success! AppImage created: ${OUTPUT_NAME}${NC}"
    echo -e "${GREEN}Size: $(du -h "${OUTPUT_NAME}" | cut -f1)${NC}"
    echo -e "\n${YELLOW}To run it:${NC}"
    echo -e "  ./${OUTPUT_NAME}"
    echo -e "\n${YELLOW}To install system-wide:${NC}"
    echo -e "  sudo mv ${OUTPUT_NAME} /usr/local/bin/${APP_NAME}.AppImage"
    echo -e "  sudo chmod +x /usr/local/bin/${APP_NAME}.AppImage"
else
    echo -e "\n${RED}Error: Failed to create AppImage${NC}"
    exit 1
fi
