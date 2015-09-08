#!/usr/bin/env python3

import os
from collections.abc import Sequence
from decimal import Decimal, ROUND_CEILING
import yaml
from PIL import Image


class Workspace:
    def __init__(self, name, screens):
        assert isinstance(name, str)
        assert isinstance(screens, Sequence)
        self.name = name
        self.screens = {}
        for s in screens:
            screen = Screen(**s)
            self._align_screen(screen)
            self.screens[screen.name] = screen

    @property
    def w(self):
        return max(s.x + s.w for s in self.screens.values())

    @property
    def h(self):
        return max(s.y + s.h for s in self.screens.values())

    def _parse_alignment(self, val):
        try:
            align, ref = val.split(maxsplit=1)
        except ValueError:
            raise ValueError('invalid alignment string: {}'.format(val))
        try:
            ref = self.screens[ref]
        except KeyError:
            raise ValueError('unknown screen name: {}'.format(ref))
        return align, ref

    def _align_screen(self, screen):
        if type(screen.x) == str:
            align, ref = self._parse_alignment(screen.x)
            if align == 'left':
                screen.x = ref.x + ref.w
            elif align == 'center':
                screen.x = ref.x + ref.w
            elif align == 'right':
                screen.x = ref.x - screen.w
            else:
                raise ValueError('invalid alignment: {}'.format(align))
        if type(screen.y) == str:
            align, ref = self._parse_alignment(screen.y)
            if align == 'top':
                screen.y = ref.y + ref.h
            elif align == 'center':
                screen.y = ref.y + ref.h
            elif align == 'bottom':
                screen.y = ref.y - screen.h
            else:
                raise ValueError('invalid alignment: {}'.format(align))

    def combine(self, images):
        workspace = Image.new('RGB', (self.w, self.h), 'black')
        for s in self.screens.values():
            try:
                img_fname = images[s.name]
            except KeyError:
                raise KeyError('missing setup for screen: {}'.format(s.name))
            img = s.prepare_image(img_fname)
            workspace.paste(img, (s.x, s.y))
        return workspace


class Screen:
    def __init__(self, name, x, y, w, h):
        assert isinstance(name, str)
        assert isinstance(x, (int, str))
        assert isinstance(y, (int, str))
        assert isinstance(w, int)
        assert isinstance(h, int)
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def prepare_image(self, filename):
        _to_int = lambda x: int(x.to_integral_value(ROUND_CEILING))
        img = Image.open(filename)
        # Best fit scale (resize and crop at center)
        i_w, i_h = img.size
        ratio = max(
            Decimal(self.w) / Decimal(i_w),
            Decimal(self.h) / Decimal(i_h)
        )
        n_w = i_w * ratio
        n_h = i_h * ratio
        img = img.resize((_to_int(n_w), _to_int(n_h)), Image.ANTIALIAS)
        d_x = _to_int((n_w - self.w) / 2)
        d_y = _to_int((n_h - self.h) / 2)
        img = img.crop((d_x, d_y, d_x + self.w, d_y + self.h))
        return img


def load_config(filename):
    with open(filename) as f:
        return yaml.safe_load(f)


def main():
    config = load_config('config.yml')
    workspaces = {}
    for w in config['workspaces']:
        workspace = Workspace(**w)
        workspaces[workspace.name] = workspace

    for i, c in enumerate(config['combine'], config['start']):
        filename = os.path.join(
            config['out_path'],
            config['name_pattern'].format(i)
        )
        print('Creating {}'. format(filename))
        workspace = workspaces[c['workspace']]
        img = workspace.combine(c['images'])
        img.save(filename)


if __name__ == '__main__':
    main()
