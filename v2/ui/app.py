# ui/app.py
import customtkinter as ctk
from ui.views.query_view import QueryView
from ui.views.config_view import ConfigView
from handlers.search import SearchHandler


class MetaCSEApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MetaCSE v1.0.0 - Polylanger")
        self.geometry("1024x768")
        self.minsize(1024, 768)

        # 初始化核心组件
        self.search_handler = SearchHandler()
        self.storage_vars = {"csv": ctk.BooleanVar(value=True), "mysql": ctk.BooleanVar(), "sqlite": ctk.BooleanVar()}

        # 构建主界面
        self._create_main_frame()
        self._create_tab_view()
        self._create_footer()

    def _create_main_frame(self):
        """创建主容器"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _create_tab_view(self):
        """创建标签页容器"""
        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.pack(fill="both", expand=True)

        # 添加标签页
        self.tab_view.add("查询")
        self.tab_view.add("配置")
        self.tab_view.add("帮助")

        # 配置标签样式
        self.tab_view.configure(
            segmented_button_selected_color="#3498db", segmented_button_selected_hover_color="#2980b9"
        )

        # 构建各标签页内容
        self._build_query_tab()
        self._build_config_tab()

    def _build_query_tab(self):
        """构建查询页"""
        tab = self.tab_view.tab("查询")
        self.query_view = QueryView(tab, self.search_handler)
        self.query_view.frame.pack(fill="both", expand=True)

    def _build_config_tab(self):
        """构建配置页"""
        tab = self.tab_view.tab("配置")
        self.config_view = ConfigView(tab)
        self.config_view.frame.pack(fill="both", expand=True)

    def _create_footer(self):
        """创建页脚"""
        footer = ctk.CTkFrame(self.main_frame, height=30)
        footer.pack(fill="x", pady=5)

        footer_text = "Version: v1.0.0 | Author: Polylanger | E-mail: qiang.zhangcs@outlook.com"
        ctk.CTkLabel(footer, text=footer_text, text_color="#666").pack(pady=3)
