# ui/query_view.py
import customtkinter as ctk
from ui.components.multiselect_dropdown import MultiSelectDropdown
from ui.components.params_row import QueryParamRow
from ui.components.table import DataTable


class QueryView:
    def __init__(self, master, search_handler):
        self.frame = ctk.CTkFrame(master)
        self.search_handler = search_handler
        self._build_ui()

    def _build_ui(self):
        # 参数配置容器
        param_container = ctk.CTkFrame(self.frame)
        param_container.pack(fill="x", padx=10, pady=10)

        params_config = [
            ("线程数:", ["5", "1", "10", "20", "30"]),
            ("查询页数:", ["1", "2", "3", "5", "10", "15"]),
            ("模式:", ["主机搜索"]),
            ("存储模式:", ["不保存", "本地存储", "云存储"]),
        ]
        self.param_row = QueryParamRow(param_container, params_config)
        self.param_row.pack(fill="x", padx=10, pady=10)

        # 搜索引擎选择
        engine_frame = ctk.CTkFrame(param_container)
        engine_frame.pack(side="left", padx=10)
        ctk.CTkLabel(engine_frame, text="搜索引擎:").pack(side="left", padx=5)
        self.engine_selector = MultiSelectDropdown(
            engine_frame, options=["Fofa", "Shodan", "Hunter", "Zoomeye", "360Quake"], width=180
        )
        self.engine_selector.pack(side="right", padx=5)

        # 查询输入
        query_row = ctk.CTkFrame(self.frame, fg_color="transparent")
        query_row.pack(fill="x", padx=10, pady=10)
        self._build_query_input(query_row)

        # 数据表格
        self.table = DataTable(
            self.frame,
            columns=("ID", "engine", "IP", "PORT/DOMAIN", "OS", "TITLE"),
            col_proportions=[0.08, 0.15, 0.22, 0.1, 0.15, 0.3],
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_query_input(self, master):
        self.query_var = ctk.StringVar(value='title="后台" && city="beijing"')

        ctk.CTkLabel(master, text="查询语句：").pack(side="left")
        entry = ctk.CTkEntry(master, width=600, textvariable=self.query_var, placeholder_text="输入查询语句...")
        entry.pack(side="left", padx=5, expand=True)

        btn = ctk.CTkButton(master, text="查询", width=80, command=self.on_query_click)
        btn.pack(side="left")

    def on_query_click(self):
        query_params = {
            "query": self.query_var.get(),
            "search_engine": self.engine_selector.get_selected(),
            **self.param_row.get_params(),
        }
        data = self.search_handler.execute_search(query_params)
        self.table.update_data(data)
