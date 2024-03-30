#[allow(clippy::wildcard_imports)]
use ratatui::{
    prelude::*,
    widgets::{*},
};

use vec_to_array::vec_to_array;
use crate::app::RAM_TIMES;

use crate::app::App;

/// Renders the user interface widgets.
pub fn render(app: &mut App, frame: &mut Frame) {
    let chunks = Layout::vertical([Constraint::Length(3), Constraint::Min(0)]).split(frame.size());
    let tabs = app
        .tabs
        .titles
        .iter()
        .map(|t| text::Line::from(Span::styled(*t, Style::default().fg(Color::Green))))
        .collect::<Tabs>()
        .block(Block::default().borders(Borders::ALL).title(app.title))
        .highlight_style(Style::default().fg(Color::Yellow))
        .select(app.tabs.index);
    frame.render_widget(tabs, chunks[0]);
    match app.tabs.index {
        0 => draw_first_tab(frame, app, chunks[1]),
        1 => draw_second_tab(frame, app, chunks[1]),
        2 => draw_third_tab(frame, app, chunks[1]),
        _ => {}
    };
}

fn draw_first_tab(frame: &mut Frame, app: &mut App, area: Rect) {
    draw_peer_list(frame, app, Rect::new(0, 0, frame.size().width, frame.size().height*3/4));
    // draw_ram_usage(frame, app, Rect::new(0, frame.size().height*3/4, frame.size().width, frame.size().height/4));
}

fn draw_second_tab(frame: &mut Frame, app: &mut App, area: Rect) {
    draw_peer_list(frame, app, Rect::new(0, 0, frame.size().width, frame.size().height*3/4));
    // draw_ram_usage(frame, app, Rect::new(0, frame.size().height*3/4, frame.size().width, frame.size().height/4));
}

fn draw_third_tab(frame: &mut Frame, app: &mut App, area: Rect) {
    draw_peer_list(frame, app, Rect::new(0, 0, frame.size().width, frame.size().height*3/4));
    // draw_ram_usage(frame, app, Rect::new(0, frame.size().height*3/4, frame.size().width, frame.size().height/4));
}

fn draw_peer_list(frame: &mut Frame, app: &mut App, area: Rect) {
    let mut table_state = TableState::default();
    frame.render_stateful_widget(
        Table::new(
            app.peers.iter().map(|peer| {
                Row::new(vec![peer.id.clone(), peer.uri.clone(), peer.gas.to_string()])
            }).collect::<Vec<Row>>(),
            [
                Constraint::Length(30),
                Constraint::Length(30),
                Constraint::Length(30),
            ]
        )
        .header(
            Row::new(vec![
                Cell::from("Id"),
                Cell::from("Main URI"),
                Cell::from("Gas on it")
            ])
        )
        .block(
            Block::bordered()
                .title("PEERS")
                .title_alignment(Alignment::Center)
                .border_type(BorderType::Thick),
        )
        .style(Style::default().fg(Color::Cyan).bg(Color::Black)),
        area,
        &mut table_state
    );
}

fn draw_ram_usage(frame: &mut Frame, app: &mut App, area: Rect) {
    let ram_usage_arr: [u64; RAM_TIMES]  = {
        if app.ram_usage.len() > RAM_TIMES {
            let ram_usage_vector = app.ram_usage.clone()[(app.ram_usage.len() - RAM_TIMES)..].to_vec();
            let ram_usage_arr: [u64; RAM_TIMES]  = vec_to_array!(ram_usage_vector, u64, RAM_TIMES);
            ram_usage_arr
        }else {
            [0; RAM_TIMES]
        }
    };
    frame.render_widget(
        Sparkline::default()
            .block(Block::default().title("Sparkline").borders(Borders::ALL))
            .data(&ram_usage_arr)
            .max(100)
            .direction(RenderDirection::LeftToRight)
            .style(Style::default().light_yellow().on_white())
        .block(
            Block::bordered()
                .title("Ram usage")
                .title_alignment(Alignment::Center)
                .border_type(BorderType::Thick),
        )
        .style(Style::default().fg(Color::Cyan).bg(Color::Black)),
        area
    );
}