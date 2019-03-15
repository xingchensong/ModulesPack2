# modulespack2
modulespack version2

This is a Framework-Plugin that helps your Web API implement modular calls.

这是一个可以实现**子功能模块化**的 Web API框架插件

modulespack的设计来源于这样的需求：
很多语音模型并不是端到端进行的，比如传统的ASR就需要先经过声学模型，然后再通过语言模型才能最终得到最终的识别结果，再比如一个训练好的Voice Conversion模型只负责把源语谱图转换为目标说话人语谱图，而前期处理过程(将音频转换为spec)和后期处理过程(将spec转换为音频，也就是Vocoder)是独立于VC的模型进行的，此时如果想要对外提供完整的VC服务，就必须经过这三个子过程，而modulespack要做的就是对这三个子功能进行**封装**



使用django + modulespack2 搭建的Voice Conversion服务平台：https://github.com/stephen-song/django_with_modulespack2
