import customtkinter as ctk
from ui.styles import UIStyler
from ui.components.table import DataTable
from handlers.search import SearchHandler
from ui.components.params_row import QueryParamRow
from ui.components.multiselect_dropdown import MultiSelectDropdown


class MetaCSEApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MetaCSE v1.0.0 - Polylanger")
        self.geometry("1024x768")
        self.minsize(1024, 768)
        self.styler = UIStyler()

        # 查询变量
        self.query_var = ctk.StringVar(value='title="后台" && city="beijing"')

        # 控件变量
        self.thread_var = ctk.StringVar(value="5")
        self.page_var = ctk.StringVar(value="1")
        self.mode_var = ctk.StringVar(value="主机搜索")
        self.storage_var = ctk.StringVar(value="不保存")
        self.engine_var = ctk.StringVar(value="Fofa")
        # 主界面布局
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 初始化界面组件
        # 提前初始化存储变量字典
        self.storage_vars = {
            "csv": ctk.BooleanVar(value=True),
            "mysql": ctk.BooleanVar(value=False),
            "sqlite": ctk.BooleanVar(value=False),
        }

        self.create_tab_view()
        self.create_footer()
        self.build_config_tab()
        
        self.search_handler = SearchHandler()

    def create_tab_view(self):
        """创建标签页容器"""
        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.pack(fill="both", expand=True)

        # 添加标签页
        self.tab_view.add("查询")
        self.tab_view.add("配置")
        self.tab_view.add("帮助")

        self.tab_view.configure(
            segmented_button_selected_color="#3498db", segmented_button_selected_hover_color="#2980b9"
        )

        # 构建查询页
        self.build_query_tab()

    def build_query_tab(self):
        """构建查询标签页内容"""
        tab = self.tab_view.tab("查询")

        # 主参数容器
        param_container = ctk.CTkFrame(tab)
        param_container.pack(fill="x", padx=10, pady=10, anchor="nw")

        # 参数配置
        params_config = [
            ("线程数:", ["5", "1", "10", "20", "30"]),
            ("查询页数:", ["1", "2", "3", "5", "10", "15"]),
            ("模式:", ["主机搜索"]),
            ("存储模式:", ["不保存", "本地存储", "云存储"]),
            # ("搜索引擎:", ["Fofa", "ZoomEye", "Shodan"]),
        ]
        self.param_row = QueryParamRow(param_container, params_config)
        self.param_row.pack(fill="x", padx=10, pady=10)

        # 搜索引擎多选组件
        engine_frame = ctk.CTkFrame(param_container)
        engine_frame.pack(side="left", padx=10)
        ctk.CTkLabel(engine_frame, text="搜索引擎:").pack(side="left", padx=5)
        self.engine_selector = MultiSelectDropdown(
            engine_frame, options=["Fofa", "Shodan", "Hunter", "Zoomeye", "360Quake"], width=180  # 增加宽度显示更多内容
        )
        self.engine_selector.pack(side="right", padx=5)

        # 查询输入行
        query_row = ctk.CTkFrame(tab, fg_color="transparent")
        query_row.pack(fill="x", padx=10, pady=10)
        self._build_query_input(query_row)

        # 数据表格
        self.table = DataTable(
            tab,
            columns=("ID", "engine", "IP", "PORT/DOMAIN", "OS", "TITLE"),
            col_proportions=[0.08, 0.15, 0.22, 0.1, 0.15, 0.3],
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_query_input(self, master):
        """构建查询输入组件"""
        ctk.CTkLabel(master, text="查询语句：").pack(side="left")
        entry = ctk.CTkEntry(master, width=600, textvariable=self.query_var, placeholder_text="输入查询语句...")
        entry.pack(side="left", padx=5, expand=True)

        btn = ctk.CTkButton(master, text="查询", width=80, command=self.on_query_click)
        btn.pack(side="left")

    def on_query_click(self):
        """处理查询事件"""
        query_params = {
            "query": self.query_var.get(),
            "search_engine": self.engine_selector.get_selected(),
            **self.param_row.get_params(),
        }
        # 模拟搜索并更新表格
        data = self.search_handler.execute_search(query_params)
        self.table.update_data(data)

    def create_footer(self):
        """创建页脚"""
        footer = ctk.CTkFrame(self.main_frame, height=30)
        footer.pack(fill="x", pady=5)

        text = "Version: v1.0.0 | Author: Polylanger | E-mail: qiang.zhangcs@outlook.com"
        ctk.CTkLabel(footer, text=text, text_color="#666").pack(pady=3)

    def build_config_tab(self):
        """重构后的配置页核心布局"""
        tab = self.tab_view.tab("配置")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        # 主容器（减少上下边距）
        main_panel = ctk.CTkFrame(tab, fg_color="transparent")
        main_panel.pack(fill="both", expand=True, padx=10, pady=5)

        # 左右面板高度同步
        left_panel = ctk.CTkFrame(main_panel, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=5)

        right_panel = ctk.CTkFrame(main_panel, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=5)

        # 构建组件（增加布局密度）
        self._build_engine_config(left_panel)
        self._build_storage_config(right_panel)
        self._build_global_actions(tab)

    def _create_section_frame(self, master, title):
        """紧凑型分区框架"""
        frame = ctk.CTkFrame(master, corner_radius=6)
        frame.pack(fill="both", expand=True, pady=3, padx=2)

        # 紧凑型标题栏
        header = ctk.CTkFrame(frame, height=28, fg_color="#2c3e50")
        header.pack(fill="x", pady=(0, 3))
        ctk.CTkLabel(
            header, text=title, text_color="#ffffff", font=("Microsoft YaHei", 12, "bold")  # 增大标题字号
        ).pack(side="left", padx=8)

        return frame

    def _build_engine_config(self, master):
        """搜索引擎动态配置区（修复版）"""
        frame = self._create_section_frame(master, "⚙️ 引擎配置")

        # 引擎选择导航栏
        self.engine_tabs = ctk.CTkTabview(frame)
        self.engine_tabs.pack(fill="both", expand=True, padx=10, pady=5)

        # 引擎配置定义
        engine_configs = {
            "Fofa": ["API Key", "API Secret"],
            "Zoomeye": ["API Key"],
            "Shodan": ["API Key"],
            "360Quake": ["API Key"],
            "Hunter": ["API Key", "Search Token"],
        }

        # 先创建所有选项卡
        for engine_name in engine_configs.keys():
            self.engine_tabs.add(engine_name)

        # 构建每个引擎的配置页
        for engine_name, fields in engine_configs.items():
            tab_frame = self.engine_tabs.tab(engine_name)
            self._build_engine_tab(tab_frame, engine_name, fields)

        # 状态指示器
        status_bar = ctk.CTkFrame(frame, height=30)
        status_bar.pack(fill="x", pady=(5, 0))
        self.api_status = ctk.CTkLabel(status_bar, text="✅ 已配置引擎: 0/5")
        self.api_status.pack(side="left", padx=10)

    def _build_engine_tab(self, master, engine_name, fields):
        """紧凑引擎配置页"""
        scroll_frame = ctk.CTkScrollableFrame(master)
        scroll_frame.pack(fill="both", expand=True)

        for field in fields:
            var_name = f"{engine_name.lower()}_{field.lower().replace(' ', '_')}_var"
            if not hasattr(self, var_name):
                setattr(self, var_name, ctk.StringVar())

            # 紧凑行布局
            row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                row, text=f"{field}:", width=100, anchor="e", font=("Microsoft YaHei", 11)
            ).pack(  # 增大标签字号
                side="left", padx=5
            )

            ctk.CTkEntry(
                row,
                textvariable=getattr(self, var_name),
                placeholder_text=f"输入{engine_name}的{field}...",
                font=("Microsoft YaHei", 11),  # 统一输入框字号
                height=28,  # 减小输入框高度
                border_width=1,
                corner_radius=4,
            ).pack(side="right", expand=True, fill="x")

    def _build_storage_config(self, master):
        """紧凑存储配置"""
        frame = self._create_section_frame(master, "💾 存储配置")

        # 存储卡片紧凑布局
        self.storage_cards = {
            "csv": self._create_storage_card(frame, "CSV", [("文件路径", "csv_path_var", "results.csv")]),
            "mysql": self._create_storage_card(
                frame,
                "MySQL",
                [
                    ("主机", "mysql_host_var", "localhost"),
                    ("端口", "mysql_port_var", "3306"),
                    ("数据库", "mysql_db_var", "metacse"),
                    ("用户名", "mysql_user_var"),
                    ("密码", "mysql_pass_var", True),
                ],
            ),
            "sqlite": self._create_storage_card(frame, "SQLite", [("数据库路径", "sqlite_path_var", "data.db")]),
        }

    def _create_storage_card(self, master, title, fields):
        """紧凑型存储卡片"""
        card = ctk.CTkFrame(master, border_width=1, border_color="#bdc3c7")
        card.pack(fill="x", pady=3)

        # 紧凑标题行
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", pady=2)
        ctk.CTkCheckBox(
            header,
            text=title,
            font=("Microsoft YaHei", 11),  # 增大复选框字号
            variable=self.storage_vars[title.lower()],
        ).pack(side="left", padx=5)

        # 动态内容区域
        content = ctk.CTkFrame(card, fg_color="transparent")
        for field in fields:
            self._create_form_row(content, *field)
        content.pack(fill="x", padx=5, pady=3)

        return card

    def _build_storage_tab(self, master, storage_type):
        """构建存储配置页"""
        config_map = {
            "csv": [("文件路径", "csv_path_var", "results.csv")],
            "mysql": [
                ("主机地址", "mysql_host_var", "localhost"),
                ("端口", "mysql_port_var", "3306"),
                ("数据库名", "mysql_db_var", "metacse"),
                ("用户名", "mysql_user_var"),
                ("密码", "mysql_pass_var"),
            ],
            "sqlite": [("数据库路径", "sqlite_path_var", "data.db")],
        }

        for field in config_map.get(storage_type, []):
            self._create_form_row(master, *field)

    def _build_csv_card(self, master):
        """CSV存储配置"""
        card = ctk.CTkFrame(master, border_width=1, border_color="#e0e0e0")
        header = ctk.CTkFrame(card, fg_color="#f5f5f5")
        header.pack(fill="x")
        ctk.CTkCheckBox(header, text="CSV存储", variable=self.storage_vars["csv"]).pack(side="left")

        content = ctk.CTkFrame(card)
        self._create_form_row(content, "文件路径:", "csv_path_var", "results.csv")
        content.pack(fill="x", padx=5, pady=5)
        return card

    def _build_mysql_card(self, master):
        """MySQL存储配置"""
        card = ctk.CTkFrame(master, border_width=1, border_color="#e0e0e0")
        header = ctk.CTkFrame(card, fg_color="#f5f5f5")
        header.pack(fill="x")
        ctk.CTkCheckBox(header, text="MySQL存储", variable=self.storage_vars["mysql"]).pack(side="left")

        content = ctk.CTkFrame(card)
        fields = [
            ("主机:", "mysql_host_var", "localhost"),
            ("端口:", "mysql_port_var", "3306"),
            ("数据库:", "mysql_db_var", "metacse"),
            ("用户名:", "mysql_user_var"),
            ("密码:", "mysql_pass_var"),
        ]
        for field in fields:
            self._create_form_row(content, *field)
        content.pack(fill="x", padx=5, pady=5)
        return card

    def _build_sqlite_card(self, master):
        """SQLite存储配置"""
        card = ctk.CCTkFrame(master, border_width=1, border_color="#e0e0e0")
        header = ctk.CTkFrame(card, fg_color="#f5f5f5")
        header.pack(fill="x")
        ctk.CTkCheckBox(header, text="SQLite存储", variable=self.storage_vars["sqlite"]).pack(side="left")

        content = ctk.CTkFrame(card)
        self._create_form_row(content, "数据库路径:", "sqlite_path_var", "data.db")
        content.pack(fill="x", padx=5, pady=5)
        return card

    def _toggle_storage_card(self):
        """动态显示存储配置卡片"""
        for storage_type, card in self.storage_cards.items():
            if self.storage_vars[storage_type].get():
                card.pack(fill="x", pady=5, before=self.storage_cards["sqlite"])
            else:
                card.pack_forget()

    def _build_global_actions(self, master):
        """全局操作区"""
        action_bar = ctk.CTkFrame(master, height=40)
        action_bar.pack(fill="x", pady=10)

        buttons = [
            ("💾 保存配置", "#4CAF50", self.on_save_config),
            ("🔄 刷新状态", "#2196F3", self.on_refresh_status),
            ("⚡ 测试连接", "#FF9800", self.on_test_connections),
            ("🧹 清除缓存", "#9E9E9E", self.on_clear_cache),
        ]

        for text, color, cmd in buttons:
            btn = ctk.CTkButton(
                action_bar, text=text, fg_color=color, hover_color=self._darken_color(color), corner_radius=8, width=120
            )
            btn.pack(side="left", padx=10)

    def _create_form_row(self, master, label, var_name, default="", is_password=False):
        """紧凑表单行"""
        row = ctk.CTkFrame(master, fg_color="transparent")
        row.pack(fill="x", pady=1)  # 减少行间距

        if not hasattr(self, var_name):
            setattr(self, var_name, ctk.StringVar(value=default))

        ctk.CTkLabel(
            row, text=label, width=80, anchor="e", font=("Microsoft YaHei", 11)  # 减小标签宽度  # 统一字体
        ).pack(side="left", padx=3)

        ctk.CTkEntry(
            row,
            textvariable=getattr(self, var_name),
            show="•" if is_password else "",
            font=("Microsoft YaHei", 11),
            height=28,  # 减小输入框高度
            border_width=1,
            corner_radius=4,
        ).pack(side="right", expand=True, fill="x", padx=3)

    def _create_form_row(self, master, label, var_name, default="", is_password=False):
        """创建标准表单行"""
        row = ctk.CTkFrame(master, fg_color="transparent")
        row.pack(fill="x", pady=2)

        if not hasattr(self, var_name):
            setattr(self, var_name, ctk.StringVar(value=default))

        # 标签部分
        ctk.CTkLabel(row, text=label, width=100, anchor="e", font=("Microsoft YaHei", 10)).pack(side="left", padx=5)

        # 输入字段
        entry = ctk.CTkEntry(
            row,
            textvariable=getattr(self, var_name),
            show="•" if is_password else "",
            border_color="#ddd",
            fg_color="#ffffff",
            text_color="#333",
        )
        entry.pack(side="right", expand=True, fill="x", padx=5)

    # 在类中添加以下事件处理方法
    def on_refresh_status(self):
        """刷新配置状态"""
        # 示例实现：统计已配置的引擎
        active_count = sum(
            1
            for engine in ["fofa", "zoomeye", "shodan", "360quake", "hunter"]
            if getattr(self, f"{engine}_api_key_var").get()
        )
        self.api_status.configure(text=f"✅ 已配置引擎: {active_count}/5")

    def on_test_connections(self):
        """测试所有连接"""
        # 示例实现：测试数据库连接
        if self.storage_vars["mysql"].get():
            print("Testing MySQL connection...")

        # 测试API连接
        current_tab = self.engine_tabs.get()
        print(f"Testing {current_tab} API connection...")

    def on_clear_cache(self):
        """清除缓存数据"""
        # 示例实现
        print("Cleaning cache files...")
        self.table.clear_data()

    def on_save_config(self):
        """保存配置到文件"""
        # 实现配置保存逻辑
        config = {
            "fofa": {"api_key": self.fofa_api_key_var.get(), "api_secret": self.fofa_api_secret_var.get()},
            # 其他引擎配置...
        }
        print("Configuration saved.")

    def on_load_config(self):
        """从文件加载配置"""
        # 实现配置加载逻辑
        print("Configuration loaded.")

    def _darken_color(self, hex_color, factor=0.8):
        """生成深色版本的颜色"""
        rgb = [int(hex_color[i : i + 2], 16) for i in (1, 3, 5)]
        darker = [int(c * factor) for c in rgb]
        return f"#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}"


if __name__ == "__main__":
    app = MetaCSEApp()
    app.mainloop()
