# ui/components/engine_tab.py
import customtkinter as ctk
from typing import TypedDict, Literal, Optional, Dict
from .form_row import FormRow

class FieldConfig(TypedDict):
    label: str
    field_type: Literal['text', 'password', 'filepath']
    default: Optional[str]

class EngineConfigTab(ctk.CTkScrollableFrame):
    """重构后的引擎配置选项卡组件"""
    
    def __init__(
        self,
        master,
        engine_name: str,
        fields: Dict[str, FieldConfig],
        **kwargs
    ):
        """
        :param engine_name: 引擎名称 (如 "Fofa")
        :param fields: 字段配置字典 {field_key: FieldConfig}
        """
        super().__init__(master, **kwargs)
        self.engine_name = engine_name.lower().replace(' ', '_')
        self.fields = fields
        
        # 初始化配置存储
        self._config_data: Dict[str, ctk.StringVar] = {}
        self._init_config_vars()
        
        self._build_ui()

    def _init_config_vars(self):
        """初始化配置变量"""
        for field_key, config in self.fields.items():
            self._config_data[field_key] = ctk.StringVar(
                value=config.get("default", "")
            )

    def _build_ui(self):
        """构建界面布局"""
        for field_key, config in self.fields.items():
            self._create_form_row(field_key, config)

    def _create_form_row(self, field_key: str, config: FieldConfig):
        """创建配置行"""
        FormRow(
            master=self,
            label=config["label"],
            variable=self._config_data[field_key],
            is_password=(config["field_type"] == "password"),
            placeholder=f"输入{self.engine_name}的{config['label']}...",
            file_browse=(config["field_type"] == "filepath")
        ).pack(fill="x", pady=2)

    @property
    def config(self) -> Dict[str, str]:
        """获取当前配置"""
        return {
            f"{self.engine_name}_{k}": v.get()
            for k, v in self._config_data.items()
        }

    def set_config(self, data: Dict[str, str]):
        """应用配置数据"""
        for k, v in data.items():
            if k in self._config_data:
                self._config_data[k].set(v)