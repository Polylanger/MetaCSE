# ui/components/form_row.py
import customtkinter as ctk
from tkinter import filedialog
from typing import Optional, Union, Callable

class FormRow(ctk.CTkFrame):
    def __init__(
        self,
        master,
        label: str,
        is_password: bool = False,
        default_value: str = "",
        placeholder: Optional[str] = None,
        variable: Optional[ctk.StringVar] = None,
        file_browse: bool = False,
        file_type: str = "file",  # "file" | "directory"
        file_ext: str = "*",
        **kwargs
    ):
        """
        增强型表单行组件
        
        :param file_browse: 启用文件浏览按钮
        :param file_type: 浏览类型 ("file" | "directory")
        :param file_ext: 文件类型过滤 (示例: "*.txt;*.csv")
        """
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # 初始化配置
        self._variable = variable or ctk.StringVar(value=default_value)
        self.file_type = file_type
        self.file_ext = file_ext
        
        self._build_widgets(label, is_password, placeholder, file_browse)
        self.pack(fill="x", pady=2)

    def _build_widgets(self, label: str, is_password: bool, placeholder: Optional[str], file_browse: bool):
        """构建组件布局"""
        # 标签部分
        ctk.CTkLabel(
            self,
            text=label,
            width=100,
            anchor="e",
            font=("Microsoft YaHei", 11)
        ).pack(side="left", padx=5)

        # 输入控件容器
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(side="right", expand=True, fill="x")

        # 输入框
        self.entry = ctk.CTkEntry(
            input_frame,
            textvariable=self._variable,
            show="•" if is_password else "",
            placeholder_text=placeholder,
            font=("Microsoft YaHei", 11),
            height=28,
            border_width=1,
            corner_radius=4
        )
        self.entry.pack(side="left", expand=True, fill="x")

        # 文件浏览按钮
        if file_browse:
            ctk.CTkButton(
                input_frame,
                text="浏览",
                width=60,
                command=self._handle_file_browse,
                font=("Microsoft YaHei", 10),
                fg_color="#4CAF50",
                hover_color="#45a049"
            ).pack(side="right", padx=(5,0))

    def _handle_file_browse(self):
        """处理文件浏览操作"""
        if self.file_type == "directory":
            path = filedialog.askdirectory(title="选择目录")
        else:
            path = filedialog.askopenfilename(
                title="选择文件",
                filetypes=[("相关文件", self.file_ext.split(";"))]
            )
        
        if path:
            self._variable.set(path)

    @property
    def value(self) -> str:
        return self._variable.get()

    @value.setter
    def value(self, val: Union[str, int, float]):
        self._variable.set(str(val))

    def clear(self):
        self._variable.set("")