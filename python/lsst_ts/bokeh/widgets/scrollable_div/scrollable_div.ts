// The "core/properties" module has all the property types
import * as p from "core/properties"

// HTML construction and manipulation functions
import {StyleSheetLike} from "core/dom"

// We will subclass in JavaScript from the same class that was subclassed
// from in Python
import {Div, DivView} from "models/widgets/div"

declare function jQuery(...args: any[]): any

export type SliderData = {from: number, to: number}

// This model will actually need to render things, so we must provide
// view. The LayoutDOM model has a view already, so we will start with that
export class ScrollableDivView extends DivView {
  override model: ScrollableDiv

  override styles(): StyleSheetLike[] {
    return [
      ...super.styles()
    ]
  }

  override render(): void {
    // BokehJS Views create <div> elements by default, accessible as this.el.
    // Many Bokeh views ignore this default <div>, and instead do things
    // like draw to the HTML canvas. In this case though, we change the
    // contents of the <div>, based on the current slider value.
    super.render()



  }
}

export namespace ScrollableDiv {
  export type Attrs = p.AttrsOf<Props>

  export type Props = Div.Props & {
  }
}

export interface ScrollableDiv extends ScrollableDiv.Attrs {}

export class ScrollableDiv extends Div {
  override properties: ScrollableDiv.Props
  override __view_type__: ScrollableDivView

  constructor(attrs?: Partial<ScrollableDiv.Attrs>) {
    super(attrs)
  }

  static {
    // If there is an associated view, this is boilerplate.
    this.prototype.default_view = ScrollableDivView

    // The this.define block adds corresponding "properties" to the JS model. These
    // should basically line up 1-1 with the Python model class. Most property
    // types have counterparts, e.g. bokeh.core.properties.String will be
    // String in the JS implementation. Where the JS type system is not yet
    // as rich, you can use p.Any as a "wildcard" property type.
    this.define<ScrollableDiv.Props>(() => ({

    }))
  }
}