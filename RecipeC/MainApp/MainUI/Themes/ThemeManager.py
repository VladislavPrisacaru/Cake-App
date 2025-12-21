from PySide6.QtCore import QObject, Property, Signal

class ThemeManager(QObject):
    themeChanged = Signal()
    dummySignal = Signal()

    def __init__(self):
        super().__init__()

        self._white_theme = {
            # Sidebar
            "sidebar_bg": "#1e293b",
            "sidebar_bg_dark": "#0f172a",
            "sidebar_hover": "#ffffff",
            "sidebar_active": "#334155",
            "sidebar_text": "#94a3b8",
            "sidebar_text_active": "#ffffff",
            "sidebar_label": "#64748b",
            
            # Main area
            "background": "#f8fafc",
            "card_bg": "#ffffff",
            "card_border": "#E2E8F0",
            "card_border_dark": "#D6DDE7",
            "card_input_bg": "#f8fafc",
            "card_border_hover": "#334155",
            
            # Accent (buttons)
            "btn_primary": "#8b5cf6",
            "btn_primary_hover": "#585bf0",
            "btn_primary_pressed": "#4f46e5",
            
            # Status colors
            "price_green": "#10B981",
            "price_bg": "#D1FAE5",
            "calories_yellow": "#F59E0B",
            "calories_bg": "#FEF3C7",
            "weight_blue": "#1E40AF",
            "weight_bg": "#DBEAFE",
            "delete_red": "#DC2626",      
            "delete_bg": "#FEE2E2",
            "n_recipes_bg": "#dacbfd",
            
            # Text
            "text_primary": "#0f172a",
            "text_secondary": "#475569",
            "text_tertiary": "#64748b",
            "text_placeholder": "#94a3b8",

            "overlay_bg": "#88000000"
        }

        self._system_main_settings = {
            "font_family": "Arial",
            "font_size_small": 12,
            "font_size_normal": 16,
            "font_size_heading_small": 22,
            "font_size_heading": 30,
            "radius_big": 18,
            "radius_small": 10,
            "radius_tiny": 5
        }

        self._colors = self._white_theme

    # ------------------- Theme Set -------------------
    def setTheme(self, theme_dict):
        self._colors = theme_dict
        self.themeChanged.emit()

    # ------------------- Sidebar -------------------
    def getSidebarBG(self):
        return self._colors["sidebar_bg"]

    def getSidebarBGDark(self):
        return self._colors["sidebar_bg_dark"]
    
    def getSidebarHover(self):
        return self._colors["sidebar_hover"]

    def getSidebarActive(self):
        return self._colors["sidebar_active"]

    def getSidebarText(self):
        return self._colors["sidebar_text"]

    def getSidebarTextActive(self):
        return self._colors["sidebar_text_active"]

    def getSidebarLabel(self):
        return self._colors["sidebar_label"]

    # ------------------- Main Area -------------------
    def getBackground(self):
        return self._colors["background"]

    def getCardBG(self):
        return self._colors["card_bg"]

    def getCardBorder(self):
        return self._colors["card_border"]
    
    def getCardBorderDark(self):
        return self._colors["card_border_dark"]

    def getCardInputBG(self):
        return self._colors["card_input_bg"]
    
    def getCardBorderHover(self):
        return self._colors["card_border_hover"]

    # ------------------- Buttons -------------------
    def getBtnPrimary(self):
        return self._colors["btn_primary"]

    def getBtnPrimaryHover(self):
        return self._colors["btn_primary_hover"]
    
    def getBtnPrimaryPressed(self):
        return self._colors["btn_primary_pressed"]

    # ------------------- Status Colors -------------------
    def getPriceGreen(self):
        return self._colors["price_green"]

    def getPriceBG(self):
        return self._colors["price_bg"]

    def getCaloriesYellow(self):
        return self._colors["calories_yellow"]

    def getCaloriesBG(self):
        return self._colors["calories_bg"]

    def getWeightBlue(self):
        return self._colors["weight_blue"]

    def getWeightBG(self):
        return self._colors["weight_bg"]

    def getDeleteRed(self):
        return self._colors["delete_red"]

    def getDeleteBG(self):
        return self._colors["delete_bg"]
    
    def getNRecipesBG(self):
        return self._colors["n_recipes_bg"]

    # ------------------- Text -------------------
    def getTextPrimary(self):
        return self._colors["text_primary"]

    def getTextSecondary(self):
        return self._colors["text_secondary"]

    def getTextTertiary(self):
        return self._colors["text_tertiary"]

    def getTextPlaceholder(self):
        return self._colors["text_placeholder"]
    

    def getOverlayBG(self):
        return self._colors["overlay_bg"]

    # ------------------- Font -------------------
    def getFontFamily(self):
        return self._system_main_settings["font_family"]
    
    def getFontSizeSmall(self):
        return self._system_main_settings["font_size_small"]

    def getFontSizeNormal(self):
        return self._system_main_settings["font_size_normal"]
    
    def getFontSizeHeadingSmall(self):
        return self._system_main_settings["font_size_heading_small"]

    def getFontSizeHeading(self):
        return self._system_main_settings["font_size_heading"]

    def getRadiusBig(self):
        return self._system_main_settings["radius_big"]

    def getRadiusSmall(self):
        return self._system_main_settings["radius_small"]
    
    def getRadiusTiny(self):
        return self._system_main_settings["radius_tiny"]

    # ------------------- QML Properties -------------------

    sidebar_bg = Property(str, getSidebarBG, notify=themeChanged)
    sidebar_bg_dark = Property(str, getSidebarBGDark, notify=themeChanged)
    sidebar_hover = Property(str, getSidebarHover, notify=themeChanged)
    sidebar_active = Property(str, getSidebarActive, notify=themeChanged)
    sidebar_text = Property(str, getSidebarText, notify=themeChanged)
    sidebar_text_active = Property(str, getSidebarTextActive, notify=themeChanged)
    sidebar_label = Property(str, getSidebarLabel, notify=themeChanged)

    background = Property(str, getBackground, notify=themeChanged)
    card_bg = Property(str, getCardBG, notify=themeChanged)
    card_border = Property(str, getCardBorder, notify=themeChanged)
    card_border_dark = Property(str, getCardBorderDark, notify=themeChanged)
    card_input_bg = Property(str, getCardInputBG, notify=themeChanged)
    card_border_hover = Property(str, getCardBorderHover, notify=themeChanged)

    btn_primary = Property(str, getBtnPrimary, notify=themeChanged)
    btn_primary_hover = Property(str, getBtnPrimaryHover, notify=themeChanged)
    btn_primary_pressed = Property(str, getBtnPrimaryPressed, notify=themeChanged)

    price_green = Property(str, getPriceGreen, notify=themeChanged)
    price_bg = Property(str, getPriceBG, notify=themeChanged)
    calories_yellow = Property(str, getCaloriesYellow, notify=themeChanged)
    calories_bg = Property(str, getCaloriesBG, notify=themeChanged)
    weight_blue = Property(str, getWeightBlue, notify=themeChanged)
    weight_bg = Property(str, getWeightBG, notify=themeChanged)
    delete_red = Property(str, getDeleteRed, notify=themeChanged)
    delete_bg = Property(str, getDeleteBG, notify=themeChanged)
    n_recipes_bg = Property(str, getNRecipesBG, notify=themeChanged)

    text_primary = Property(str, getTextPrimary, notify=themeChanged)
    text_secondary = Property(str, getTextSecondary, notify=themeChanged)
    text_tertiary = Property(str, getTextTertiary, notify=themeChanged)
    text_placeholder = Property(str, getTextPlaceholder, notify=themeChanged)


    overlay_bg = Property(str, getOverlayBG, notify=themeChanged)


    font_family = Property(str, getFontFamily, notify=dummySignal)
    font_size_small = Property(int, getFontSizeSmall, notify=dummySignal)
    font_size_normal = Property(int, getFontSizeNormal, notify=dummySignal)
    font_size_heading_small = Property(int, getFontSizeHeadingSmall, notify=dummySignal)
    font_size_heading = Property(int, getFontSizeHeading, notify=dummySignal)
    radius_big = Property(int, getRadiusBig, notify=dummySignal)
    radius_small = Property(int, getRadiusSmall, notify=dummySignal)
    radius_tiny = Property(int, getRadiusTiny, notify=dummySignal)
