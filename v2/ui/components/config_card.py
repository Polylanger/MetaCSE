# ui/components/config_card.py
import customtkinter as ctk
from typing import List, Tuple, Optional
from .form_row import FormRow

class ConfigCard(ctk.CTkFrame):
    def __init__(
        self,
        master,
        title: str,
        fields_config: List[Tuple[str, str, Optional[str], bool]],  # (label, field_id, default, is_password)
        toggle_var: Optional[ctk.BooleanVar] = None,
        border_color: str = "#bdc3c7"
    ):
        super().__init__(master, border_width=1, border_color=border_color)
        
        self.title = title.lower()
        self.toggle_var = toggle_var or ctk.BooleanVar()
        self.form_rows = []
        
        # 安全解析配置
        self._validate_config(fields_config)
        
        self._build_header()
        self._build_content(fields_config)

    def _validate_config(self, configs: List[Tuple]):
        """验证配置格式"""
        if not all(len(item) >= 3 for item in configs):
            raise ValueError("每个配置项至少需要包含 (label, field_id, default)")

    def _build_header(self):
        """构建标题栏"""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=2, anchor="w")
        
        ctk.CTkCheckBox(
            header,
            text=self.title.capitalize(),
            variable=self.toggle_var,
            font=("Microsoft YaHei", 11)
        ).pack(side="left", padx=5)

    def _build_content(self, configs: List[Tuple]):
        """构建内容区域"""
        content = ctk.CTkFrame(self, fg_color="transparent")
        
        for config in configs:
            label, field_id, default, is_password = self._parse_config_item(config)
            
            row = FormRow(
                master=content,
                label=label,
                is_password=is_password,
                default_value=default or "",
                placeholder=f"输入{self.title}的{label}..."
            )
            self.form_rows.append(row)
            
        content.pack(fill="both", expand=True, padx=5, pady=3)

    def _parse_config_item(self, config: Tuple) -> Tuple:
        """安全解析配置项"""
        return (
            config[0],                   # label
            config[1],                   # field_id
            config[2] if len(config)>=3 else "",  # default
            config[3] if len(config)>=4 else False # is_password
        )

    def get_values(self) -> dict:
        """获取配置值"""
        return {
            "enabled": self.toggle_var.get(),
            "fields": {row.label: row.value for row in self.form_rows}
        }